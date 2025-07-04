import pandas as pd
import requests
import itertools
from datetime import datetime
import re
import io
import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

# Set options to display all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Optional: widen the display if needed
pd.set_option('display.width', None)

def fetch_api_tokens():
    api_tokens = [
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiOTNkOWE1NTRiNTBkMDJkZDlkYTQzMDIzYWU5OTM2ZGRkZ"
        "GEyNmU1YjRkMDYxMzFhNGFiYzc2NDNkMjY4YTYxN2ZlZjY4NjJlZWVmZjVjMTgiLCJpYXQiOjE3MzY0MzA4NjYuODkzNjM0LCJuYmYiOjE"
        "3MzY0MzA4NjYuODkzNjM5LCJleHAiOjQ4OTIxMDQ0NjYuODg4ODAzLCJzdWIiOiIxOTc0ODU3Iiwic2NvcGVzIjpbXX0.DtP-949ngXZ4N"
        "PEW9aAaPxK9pcb7WOuru35ZzDCFWv-i2OwefloSIPIn6Q75Gd7EM5-1PNp55kpl5IENS_CXI3Xo0x4P_a9YHwXerWhbylEcVauB_oE5JIV"
        "laA5d9yQhbrv7Xf2wzBMP7By0ANcpqobAl7ld_DgVF-YA5zzhvhh2itAbtnXOv8jG_K56BhfECwC9HK2J2vihVJmgxWp_n9jjZShOMnlTz"
        "Rf4OIf0bUPLtZV3tI1VlyTLoR0kBH4Osu6uYHw5QkMqAil23uuDqopHaAI-6w1U9tWuZV7PkS_tdkbjpGYgeKLdm6gpenFyVLcUzyAySoE"
        "Z2NH5eKCLg_TPOw7BxJGjY_K15UpBl0EIe59zZjtwZA_CW1QfhRAS27MwA-7TDkPNeQWNKFn8TdlsySidHI7J7lfmG0KB4793pUMjljvA3"
        "_wvh1ZKnplFQ10y_fXcmCyuQrKM44Vl6ZaLD78wQ-q_fN88tSaV4Avq1Z80XzsTfJEkfoG2Lnpa61760CyXG0v3l6R0i_U4SQk1FdwhuPp"
        "_cP3hLyu9BrFLRt4u53lMmTa_5J72rRzbGBVeZjjJBOXFy3Y9J-OM7H4u4Kz0QIZhyN3XB2lXgHy7VZcsRuQhb6X39W3Ukk0ZyuCZeEWK4"
        "mn_Uf7i9d4uiDuLalRhu-vHXpOHsyAvQl0",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMjM5Y2Q1N2I0MGI1MjBhN2Y5NGRhMzE0ZjdlMDIwMm"
        "JkMmViNDFjNjU5YTkxNjRhOTRjYWEwZjRkOTYzOTFiMjkxNzY5NzNiNzAwYTJlODIiLCJpYXQiOjE3MzM4NDczNDguOTkyNzQyLCJuY"
        "mYiOjE3MzM4NDczNDguOTkyNzQ1LCJleHAiOjE3NjUzODMzNDguOTc1NTAyLCJzdWIiOiIxOTczNjY2Iiwic2NvcGVzIjpbXX0.jgIg"
        "ZkAsB-Ncivv5lyJCQx3XvABRbIpUThmLtb7AENe0S8e3lwKSBkyE_QbrFqIYa-z4p0J42OkQz0uv-h_aepG_7OhdlKzpe3eSECZY1LE"
        "RRtqdTIsO9gBx0Wqxul7ixOaAJHdjpHCHS_eXaZKLu3_OhTEkyAD8EHILlbv6Uc3R2cOtpY5s3rJEFffcPIN7tmuZ7Mmeo9SJXpnSdb"
        "4qg6REJsO5YLFPUpvZyZn1G9SwVfpZAP0nfbrTuXKIwo6gbX22R_UZGL_n2rHnObUqKyRUdS8XCEuZfQNge6_VwT2vsb72rNMK4Dw5S"
        "m4jeQEcdbRMaB-rr0YpkFXyMAhHsV8cimfmDPro_NxUV2dXONtlfZhGFySPbAckncCZq7geMLXhP-MYOm3FxPsiI7FFw3_LsQyNICs4"
        "Hndy8ccKe_sPldWWV6eq7E2OYQcpOfrcRjk4YrnVl1fJL_krxVYvf_JwYqRb9GCpjpdBScWlKWc549HnqKtx-jD8S_QOjgDCuVgXwbg"
        "wggmcKLCb9AEAL3zcKwOSoxQ4Bqg8XMqHLiSoUs-KwHxj6bpi1xXzeaCTN84sV1jK4TO99v_bjHGkBSP9H6sbwEViPdaD9MmjMOv0C5"
        "z-PdGTf7cRQm6kee0F7Q6gk7J-nRBGV5unL0il7S9gd2UXZc7xsJV3hkm8Qws",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiNWY1NGY5NzBmMWJlNDEyNDUwZGI2ZjczMWRjNzA2NTI"
        "4NmVkMzRhMGQxMGVkODZmYzY0OWI1NWFlN2E1MWE1M2Q4M2Q2N2FhMjAwNTk2ZGIiLCJpYXQiOjE3MzY3OTAzMzQuOTYzNjE3LCJuYmYi"
        "OjE3MzY3OTAzMzQuOTYzNjIsImV4cCI6NDg5MjQ2MzkzNC45NTc0NTMsInN1YiI6IjE5NzUwNzUiLCJzY29wZXMiOltdfQ.f-nZneDlXj"
        "G8cAk8VJuvJYBw9jBToBx3cL-I2uFqTjvhoX4oqoYsAQPvTIMhOJLXwL8yYxl1bPWro7ynjx-HiZu0w5PylnZzDPWxZQlBCYluLIOIoel"
        "4_mdpZvF0Jb-755dWLkWsT9Yxn86PjwtDqDizZzXGML8r3TIwlFwD03wSMvOKdZK7Uc7x8u2NZBq4jIS7eZM0sQtM5dciyPEk8S03Z5TG"
        "MUxye2zWAp9iAXXRStdPGs1pwe3UTWIjbyMBTLMmUDuKYzixXOVmzkkyL5IiqGfrbm4fHfk4s-C4B8jnFnUpkaGtGGAaT8mdKJmjNeFla"
        "1xg3XG306TSJ7dfYDV9NyGav0okQbERSPL5wRG9m9CrgMdzad7U08MuV8glST3koHY0TZguNtL-G4m7luPfQIK26EXmrCJI2jL7keBgcU"
        "N9Pck0hmUQiCbyn01L-rC8pU6i-R4a9mqKYVtlOfDHTcSuUyPtoa1EE-WA-rSY4cLtTtRqwJUCv3_1rQ2lhMfe0TfL-DRDvwfhyxF8xy0"
        "kygYPfs83wL4UkxTZxZnsAUjv51G-302ZLqrBVLkODOSLmAWJgLBu1BsvW7bKXUwQCLcut2RfPn9OhnS75Tu3qUvAq7uXNwNPH6zw0j53"
        "9rOlHt3A4TgkFiOZzjKvBhr1WT7ZuzHWUYPvLjdv1fw",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiNTAwZmIyNDU4OWVmYmI4MWRiNmVmMmJhZmI3ODA1ZjEy"
        "ZTIyN2RjM2NhMjYzNmYzYzI1NGY3ODI5ZDlmMmFiYzEwMjllN2EwMTUyNjBiNGYiLCJpYXQiOjE3MzY4NTEzODUuNDg0MDU3LCJuYmYiO"
        "jE3MzY4NTEzODUuNDg0MDYsImV4cCI6NDg5MjUyNDk4NS40Nzk5NDUsInN1YiI6IjE5NzUxMTAiLCJzY29wZXMiOltdfQ.iXjyYV6C7zj"
        "Z6-f6KZ3EFrdS_R1ntjv4X-LgV4wZqz5wHRVM1AbotaDJi2dtuFVludJWBhXlLEu32FpsB1Ogrk0pBe2ELB3HcN6Rc80uUBHUDo8Xbtux"
        "e_dhtOcP9ZsDEltDsvSBznzGWUSqaxHu3BxpBfhlmLwzjhbA2SLkKbMo_LnlnuenpKSAxnpwExuuvY4znPLZhSBHdfdPABdkchPfCX7Js"
        "Lp58ZvMqyZ8zjJ1fRcjfpBz6VybxIW9oErtGRsXfdU5eUX6hW2MWgtNkW6iU09k_Ge4C7ag4QaQTWkLkM2DjLOoLByXm3b1URv04suYDK"
        "FGAUmO9zapAqjYJ2ljp8yrqpRnLnmr7ltQHQ-nZezUQZJDdvIM5kWANLMQEax9xPAB6EbTouXFf8X8NjiCtbAAJcPPLAHsxPX5CW9DVMW"
        "-tw1zsHC06Jg_ou3LMd-XUPilF86iXC_1pP_0dbgCDa7GZEaV_ptiQ24LqD1QSkKt7qXVvxmoO2Ktu4mJez1tzs6prThke9YiijG9FJND"
        "a4Tnj6K_DCsx_IJwaoCBFQjM7l_EaIAYTgh49nPojPGfXop-_oIxcEhJN1ZH26syhC2rARV84vQ30h1VerRWWddWP8mxjx0lIv3oRiG6v"
        "gvyR-iD9nyVW41NOykKGDv9GaAexB4PkgRJ7pjUkFw",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiYjFjZGU4ZmNiOGM2MjQxZWVkN2E3ZDk3NDhmMWJlMzgyY"
        "Tc2MmY2ZjBkZjI0NmY4MGFmZjJkMjA0NmJmYjZiZTAwM2ExNzY5YTVlYzYzMDciLCJpYXQiOjE3MzY5NTQzMDUuNjA3NzIyLCJuYmYiOjE3"
        "MzY5NTQzMDUuNjA3NzI1LCJleHAiOjQ4OTI2Mjc5MDUuNjA0MDEyLCJzdWIiOiIxOTc1MjI1Iiwic2NvcGVzIjpbXX0.oFYuSb5P0ESf7cH"
        "tHVGqR-2FMwUKycawpb_gUKAqzOzPf_-y5yri8AyK8-ssKZ7-hZn4utzMTxHmeJ8rFWCpW1rrJhI1EfrcjqDS_z4P_smbDEeIwABVLBvm4t"
        "fZCQAGwHSvt7SEIfjP_YNU5R2sF_natkqqAvqCdzmcmJoLJP6-kCO5vlOwsTKtYQhus7IKeyHbyXBqdAm5MXi85uLeeZvYlu-BIcwiN6xwe"
        "aLSyBlR44gqiliDsAbb0GmQ9IFQq2Mjmt7m3ajsVdF_HeQJVZyvSKTn_QEZ9rp40x7CwaYxsECcmBfUTWbTs5fdj3ZUznvnn6yFOFzTt0IY"
        "yvRo-v0ZDiIOMqNVJ5jzQXlBUb39YHljKVLZBQguC4UijWIOTkpGpbhLNaueO3FjwBPji0jqCIblxmyRC3QhzTEJOJcduAV8HSh7sILkWoA"
        "x05j2ShRPhu9ri2uIGZzEL2_H27CKqWIap66MCWz0npfPgH1L1LHiOKxIK9oV1X7fUJM9ol1KAHmacrT88y-JotHgKqcd1GseVWLQzlm3-o"
        "Q0-LIiwbSZOfIHSF3a8u5MGhtGrtVTEQnxubQ-rfo6IKTCWHAj_zc3DdySdsmakejZ7_JkLDP414JkGgFEiMhB9tz3weOsCavHPm80cjr2P"
        "bAb6NTWFlMTy-AyMSsq60b85jA",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiNjQ4MjQzMWI3ZWMwZGMwYTVmMWYxY2Q2ZDdjMThiZjkyOW"
        "FmYjljNDhjNmY2MDI2YTdkMWVjZjMyNWJiY2Q0MjY3MGU2ZjFmNjdkNjIxMTAiLCJpYXQiOjE3MzY5NTQzNzMuMjI1MDAzLCJuYmYiOjE3M"
        "zY5NTQzNzMuMjI1MDA3LCJleHAiOjQ4OTI2Mjc5NzMuMjIwNDM0LCJzdWIiOiIxOTc1MjI2Iiwic2NvcGVzIjpbXX0.EEs7cwr17uZ7E-Mj"
        "jYNehnhkcuWEhVF-HIQEU78pLpv0_8MxgIF0KufjHwb60hhdlh2kuNh2DKssq8F7E3aHvPXYOtrnYQvq4GBLM0Q2LeRG3dKduCdC6iBC0h4"
        "EJX3DlJ-yWfRbjmcURjAC0wPCU0_5rv89eLLZJRWAYTJIS1X1MXhvkt1fu0DsQl3PdbZ-EaWRdp88CgK9RTDtwx4V-mNLp_WrhZ541D_fbw8"
        "ZVcISMPMRRhhetDxB3mBrLkWt23A44uPS4Kq4vHPNwBxzLhIgBtdcm-PAqitFnfC4p5b9V_ntWXLTkcEY2X7LoI1xwYh8OIZaXjiLdBqJOP"
        "tifdLXaeW_diGgr6SoUngNN2WE-tY0U9PKx_Xua8-kSitMZFnwKPOmKA2CqOgLy97sG_eA1LF8bY3krYqVS8B9vnfT1_KEotcQO5LYiTM6fR"
        "vWK9Ki9CLBVmot6Bv7XYOWoF7DQgFx7jEGmWGV3HR1P1SOgDZ9ZZaOxPm8RIDUPmVrc2CocWkWTbYa0wE5KwrnzZT5GDBxJp5QCQyjQ_7rhv"
        "jMeO8FQxOqJTvIE5iKmoBDUqUr4G58XNYVdBxi9xcnsQSCHU8VRUlGdFYP0r71sFMmzQCqOY7hu84odb1aS3_vko7yynm54wfGO8auG7pgqS"
        "fRM5_84z9y4BaLzbRDyFQ"]
    return api_tokens

def fetch_hotlist_candidates(api_id, api_tokens):
    candidate_list = []

    # Ezekia URL
    base_url_agg = f"https://ezekia.com/api/projects/{api_id}/candidates?filterOn%5B%5D=fullName&sortOrder=desc&sortBy=createdAt"

    # Headers to authenticate API request for total counts
    headers = {
        "Authorization": f"Bearer {api_tokens[0]}",
        "Content-Type": "application/json"  # Adjust content type if necessary
    }

    # API request (GET request) for total counts
    page_response = requests.get(base_url_agg, headers=headers)

    # Extract "last_page" value
    last_page_candidates = page_response.json()['meta']['lastPage']

    # Loop through candidates in hotlist
    for page in range(1, last_page_candidates + 1):

        api_token = api_tokens[(page - 1) // 3 % len(api_tokens)]

        # Headers to authenticate API request for total counts
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"  # Adjust content type if necessary
        }

        page_url = f"https://ezekia.com/api/projects/{api_id}/candidates?filterOn%5B%5D=fullName&page={page}&sortOrder=desc&sortBy=createdAt"
        page_response = requests.get(page_url, headers=headers)

        for candidate_index in range(0, len(page_response.json()["data"])):

            if page_response.status_code == 200:
                # Process the data for this page (you can print or store it)
                print(f"Ezekia API ID {api_id}")
                print(f"Fetched candidate page {page} from Ezekia API")
            else:
                print(f"Failed to fetch data for page {page}. Status Code: {page_response.status_code}")

            # Candidate details
            candidate_id = page_response.json()["data"][candidate_index]["id"]
            candidate_name = page_response.json()["data"][candidate_index]["name"]
            candidate_updated = page_response.json()["data"][candidate_index]["updatedAt"]

            if len(page_response.json()["data"][candidate_index]["addresses"]) > 0:
                if page_response.json()["data"][candidate_index]["addresses"][0]["city"]:
                    candidate_city = page_response.json()["data"][candidate_index]["addresses"][0]["city"]
                else:
                    candidate_city = ''

                if page_response.json()["data"][candidate_index]["addresses"][0]["country"]:
                    candidate_country = page_response.json()["data"][candidate_index]["addresses"][0]["country"]
                else:
                    candidate_country = ''

            else:
                candidate_city = ''
                candidate_country = ''

            #candidate_address = candidate_city + ', ' + candidate_country

            # Candidate position details
            candidate_position_data = page_response.json()["data"][candidate_index]["profile"]

            # Iterate through each position and dynamically name the fields
            for index, position in enumerate(candidate_position_data['positions'], start=1):

                candidate_role_number = index

                if 'title' in position and position['title'] is not None:
                    title = position['title']
                else:
                    title = None

                if 'company' in position and position['company'] is not None and 'name' in position['company']:
                    company = position['company']['name']
                else:
                    company = None

                if 'location' in position and position['location'] is not None and 'name' in position['location']:
                    location = position['location']['name']
                else:
                    location = None
                    #location = candidate_address

                if 'startDate' in position and position['startDate'] is not None:
                    startdate = position['startDate']
                else:
                    startdate = None

                if 'endDate' in position and position['endDate'] is not None:
                    enddate = position['endDate']
                else:
                    enddate = None

                # Dynamically creating field names
                candidate_role_number = index

                # Create a dictionary with dynamically named fields and print it
                position_info = {
                    "Candidate Experience": candidate_role_number,
                    "Candidate Title": title,
                    "Candidate Company": company,
                    "Candidate Location": location,
                    "Start Date": startdate,
                    "End Date": enddate
                }

                # New key-value pair to add at the start
                candidate_dict = {'Candidate ID': candidate_id,
                                  'Candidate Name': candidate_name,
                                  'Candidate Updated At': candidate_updated}

                candidate_info = {**candidate_dict, **position_info}

                # Append extracted values to the list
                candidate_list.append(candidate_info)

    # Create a DataFrame from the list of candidate data points
    candidate_df = pd.DataFrame(candidate_list).reset_index(drop=True)
    print(candidate_df.info())

    #candidate_df['candidate_start_date'] =
    candidate_df['Candidate Location'] = candidate_df['Candidate Location'].replace('United Kingdom', 'London, UK')

    return candidate_df

# Normalize and map fallback + bracket values to final form
fallback_map = {
    'executive director': 'ED',
    'managing director': 'MD',
    'vice president': 'VP',
    'vice-president': 'VP',
    'vp': 'VP',
    'md': 'MD',
    'ed': 'ED',
    'assoc': 'As',
    'assoc.': 'As',
    'as': 'As',
    'an': 'An',
    'analyst': 'An',
    'director': 'D',
    'd': 'D',
    'ad': 'D'
}

# Normalize and map fallback + bracket values to final form
ordered_fallback_map = {
    'managing director': 'MD',
    'executive director': 'ED',
    'director': 'D',
    'vice president': 'VP',
    'vice-president': 'VP',
    'vp': 'VP',
    'md': 'MD',
    'assoc': 'As',
    'assoc.': 'As',
    'analyst': 'An'}

# Ordered list for substring matching
ordered_fallbacks = list(ordered_fallback_map.keys())

# Approved values for brackets (case-insensitive)
allowed_bracket_values = set(fallback_map.keys())


def extract_seniority(text):
    text_lower = text.lower()

    # 1. Try to extract and validate bracketed content
    bracket_match = re.search(r'\(([^)]+)\)', text)
    if bracket_match:
        bracket_value = bracket_match.group(1).strip().lower()
        if bracket_value in allowed_bracket_values:
            return fallback_map[bracket_value]

    # 2. Fallback to substring search
    for keyword in ordered_fallbacks:
        if keyword in text_lower:
            return fallback_map[keyword]

    return None  # or 'Unknown'


def fetch_candidates_additional_labels(hotlist_df_trans, api_tokens):
    candidate_id_list = list(hotlist_df_trans['Candidate ID'].unique())
    print(f"Total candidates: {len(candidate_id_list)}")

    candidates_additional_list = []
    index_counter = 0
    for index, id in enumerate(candidate_id_list):

        print(f"Project: {index} / {len(candidate_id_list)}")

        candidate_url = f"https://ezekia.com/#/people/{id}"

        # Ezekia URL for total meeting and page (api) count
        base_url_agg = f"https://ezekia.com/api/relationships?id={id}&type=person&relatedType=person"

        index_counter += 1
        api_token = api_tokens[(index_counter - 1) // 3 % len(api_tokens)]

        # Headers to authenticate API request for total counts
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"  # Adjust content type if necessary
        }

        # API request (GET request) for total counts
        response = requests.get(base_url_agg, headers=headers)

        # Initialize project_rec_label before the loop
        candidate_reports_into = None

        # Iterate through the response data
        response_data = response.json()
        if "data" in response_data and "people" in response_data["data"]:
            for person in response_data["data"]["people"]:
                if person["relationship"] == 27571:
                    candidate_reports_into = person["id"]

        # Append extracted values to the list
        candidates_additional_list.append({"Candidate ID": id, "Candidate URL": candidate_url, "Candidate Reports Into": candidate_reports_into})

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(candidates_additional_list).reset_index(drop=True)

    return df

def get_candidate_companies(group):
    group = group.sort_values(by='Candidate Experience')

    # Get company at experience 1
    company1_row = group[group['Candidate Experience'] == 1].iloc[0]
    company1 = company1_row['Candidate Company']

    # Find the first different company (≠ company1)
    different_company_rows = group[group['Candidate Company'] != company1].sort_values('Candidate Experience', ascending=True)
    if not different_company_rows.empty:
        diff_row = different_company_rows.iloc[0]
        company2 = diff_row['Candidate Company']
        company2_date = diff_row['End Date']
        company2_experience = diff_row['Candidate Experience']

        # Get all company1 rows that occurred *after* the switch (i.e. higher experience number)
        company1_prior_rows = group[
            (group['Candidate Experience'] < company2_experience) &
            (group['Candidate Company'] == company1)
        ].sort_values('Candidate Experience', ascending=False)
        
        if not company1_prior_rows.empty:
            # Choose the most recent one before the switch (i.e. lowest exp > company2 exp)
            closest_exp_row = company1_prior_rows.sort_values('Candidate Experience', ascending=False).iloc[0]
            company1_start_date = closest_exp_row['Start Date']
        else:
            company1_start_date = None
    else:
        company2 = None
        company2_date = None
        company1_start_date = None

    # Get current date
    now = datetime.now()
    
    # Ensure your date column is in datetime format
    if company1_start_date is not None:
        company1_start_date_time = pd.to_datetime(company1_start_date)
        within_year_flag = "Yes" if pd.notnull(company1_start_date_time) and (now - company1_start_date_time).days <= 365 else "No"
        within_half_year_flag = "Yes" if pd.notnull(company1_start_date_time) and (now - company1_start_date_time).days <= 182 else "No"
                                                          
    else:
        within_year_flag = None
        within_half_year_flag = None
                                                          
    return pd.Series({
        'Candidate ID': group['Candidate ID'].iloc[0],
        'Candidate Company Previous': company2,
        'Candidate Company Previous End Date': company2_date,
        'Candidate Company Start Date': company1_start_date,
        'Candidate Move Within Year': within_year_flag,
        'Candidate Move Within 6 Months': within_half_year_flag
    })


def get_disc(candidateId, token_iterator, api_id):
    # Headers to authenticate API request for total counts
    api_token = next(token_iterator)
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    page_url = f"https://ezekia.com/api/people/{candidateId}/additional-info"
    page_response = requests.get(page_url, headers=headers)

    field_ids = {
        656050: 11941,
        647987: 11817
    }

    api_id = int(api_id)

    if api_id not in field_ids:
        return None

    target_field_id = field_ids[api_id]

    # Direct access: no .get()
    for item in page_response.json()["data"]:
        if item["field"]["id"] == target_field_id:
            value = item["value"].lower() if item["value"] else ""
            if "sales" in value or "structuring" in value:
                return "Sales/Structuring"
            elif "trading" in value:
                return "Trading"

    return None  # After checking all items

def assign_type(company_name, entity_df):
    if not isinstance(company_name, str):
        return None  # or "Unknown"
    for _, row in entity_df.iterrows():
        if row['Name'].lower() in company_name.lower():
            return row['Type']
    return None  # or "Unknown"


def normalize_entity_name(text):
    bank_names = [
        "Bank of America", "Goldman Sachs", "Deutsche Bank", "Morgan Stanley", "Natixis",
        "TD Securities", "Standard Chartered", "Commerzbank", "Citi", "J.P. Morgan", "Commonwealth",
        "BMO", "ICBC", "Macquarie", "ANZ", "HSBC", "Mitsui", "BNP", "UniCredit",
        "Marex", "Lloyds"
    ]

    if not isinstance(text, str):
        return text  # keep non-string values unchanged

    text_lower = text.lower()

    for name in bank_names:
        if name.lower() in text_lower:
            return name

    return text 


# Streamlit UI
st.title("Ezekia Org Chart Inputs")

api_tokens = fetch_api_tokens()  # Fetch once

allowed_ids = {
    "647987": "HL - EMEA Metals Banking",
    "656050": "HL - EMEA Energy Banking"
}

# Generate a button per allowed API ID
for id, label in allowed_ids.items():
    if st.button(f"Fetch Profiles – {label} ({id})"):
        api_id = id  # Set api_id based on button clicked
        
        try:
            candidates = fetch_hotlist_candidates(api_id, api_tokens)
            candidates_previous = candidates.groupby('Candidate ID').apply(get_candidate_companies).reset_index(drop=True)
            candidates.drop('End Date', axis=1, inplace=True)

            candidates = candidates.merge(candidates_previous, on='Candidate ID', how='left')
            candidates = candidates[candidates['Candidate Experience'] == 1]
            candidates['Candidate Seniority'] = candidates['Candidate Title'].apply(extract_seniority)
            candidates = candidates[[ 
                "Candidate ID", "Candidate Name", "Candidate Title", "Candidate Company", "Candidate Company Start Date", "Candidate Location", 
                "Candidate Seniority", "Candidate Company Previous", "Candidate Company Previous End Date", "Candidate Move Within Year", "Candidate Move Within 6 Months"
            ]]

            candidates["Candidate Company"] = candidates["Candidate Company"].apply(normalize_entity_name)
            candidates["Candidate Company Previous"] = candidates["Candidate Company Previous"].apply(normalize_entity_name)
            
            candidates["Lucid Space"] = ""
            candidates["Lucid Space 2"] = ""

            location_map = {
                'Paris': 'Paris',
                'London': 'London',
                'New York': 'New York',
                'Singapore': 'Singapore'
            }

            for key in location_map:
                candidates.loc[candidates['Candidate Location'].str.contains(key, case=False, na=False), 'Candidate Location'] = location_map[key]

            candidate_reports_into = fetch_candidates_additional_labels(candidates, api_tokens)
            candidates_output = pd.merge(candidates, candidate_reports_into, on='Candidate ID', how='inner')

            token_iterator = itertools.cycle(api_tokens)
            candidates_output["Discipline"] = candidates_output["Candidate ID"].apply(lambda cid: get_disc(cid, token_iterator, api_id))

            entity_dict = {
                "Standard Chartered": "Bank", "ICBC": "Bank", "Bank of America": "Bank",
                "Citi": "Bank", "Macquarie": "Bank", "Goldman Sachs": "Bank",
                "Mitsui": "Bank", "BNP": "Bank", "Commerzbank": "Bank",
                "Lloyds": "Bank", "Morgan Stanley": "Bank", "Natixis": "Bank",
                "J.P. Morgan": "Bank", "UniCredit": "Bank", "Marex": "Bank",
                "Credit Suisse": "Bank", "RBC": "Bank", "ANZ": "Bank", "TD Securities": "Bank",
                "Mercuria": "Trading House", "Vitol": "Trading House", "Trafigura": "Trading House",
                "Hartree": "Trading House", "Koch": "Trading House"
            }

            entity_map = pd.DataFrame(list(entity_dict.items()), columns=["Name", "Type"])
            
            candidates_output["Current Entity Type"] = candidates_output["Candidate Company"].apply(lambda x: assign_type(x, entity_map))
            candidates_output["Previous Entity Type"] = candidates_output["Candidate Company Previous"].apply(lambda x: assign_type(x, entity_map))

            def determine_platform_type_move(row):
                current = row["Current Entity Type"]
                previous = row["Previous Entity Type"]

                if current == "Bank" and previous == "Bank":
                    return "Bank to Bank"
                elif current == "Bank" and previous == "Trading House":
                    return "Trading House to Bank"
                elif previous == "Bank" and current == "Trading House":
                    return "Bank to Trading House"
                elif current == "Hedge Fund" and previous == "Bank":
                    return "Bank to Hedge Fund"
                else:
                    return "Other"

            # Apply the function row-wise
            candidates_output["Platform Type Move"] = candidates_output.apply(determine_platform_type_move, axis=1)

            st.success(f"Data fetched successfully for {label} ({id})!")

            sheet_keys = {
                "647987": "1kDZIOe5orm-OCaeCRxtSEmVU8kkoNdF_23zNj_0GHW0",
                "656050": "1oUI2kUMCokKRJiyAR1GoeH0pd1WpkOoC3ckMaruYjfU",
                "217903": "1zK7H16AlYKsvfX-aMLWjUAqKF4wqQAtnfJSuQPRibRE",
                "659219": "1zA8qmiJ5ue73PDWaEbxijb2Fttkl7z7MfehuDLhuQnY",
                "666702": "1HxCJK19ASq18_HzncG4lbMb3_mefINZS6J3dLZjLFFg"
            }

            sheet_key = sheet_keys.get(api_id)
            
            if sheet_key:
                try:
                    scope = ["https://www.googleapis.com/auth/spreadsheets"]
                    service_account_info = dict(st.secrets["gcp_service_account"])
                    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
                    client = gspread.authorize(creds)
                    sheet = client.open_by_key(sheet_key)
                    worksheet = sheet.worksheet("LucidData")
                    worksheet.clear()
                    set_with_dataframe(worksheet, candidates_output)
                    st.success("Ezekia data sent to Google Sheets. Refresh in Lucid to view updates.")
                except Exception as e:
                    st.error(f"Google Sheets error: {e}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
        
