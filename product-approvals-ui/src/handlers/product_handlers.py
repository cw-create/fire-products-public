import os
import time

import requests
import streamlit as st
from utils.loggers import logger_name, make_logger

logger = make_logger(logger_name())

INTERNAL_API_KEY = os.environ.get("INTERNAL_API_KEY", "")
HOSTNAME = os.environ.get("HOSTNAME", "https://product-approvals-gf3dkeclfa-ww.a.run.app")
logger.info(f"HOSTNAME: {HOSTNAME}")


class ProductHandler:
    def __init__(self):
        self.base_url = f"{HOSTNAME}/public/v1"
        self.auth = (INTERNAL_API_KEY, "")

    def upload(self, st_uploaded_file):
        st.info("Uploading product...")
        start_time = time.time()

        url = f"{self.base_url}/product/upload"
        files = {
            "file": (st_uploaded_file.name, st_uploaded_file.getvalue(), st_uploaded_file.type)
        }
        response = requests.post(url, auth=self.auth, files=files)
        if response.status_code != 200:
            error_msg = f"Failed to upload file: {response.text}"
            st.error(error_msg)
            raise Exception(error_msg)

        elapsed_time = time.time() - start_time
        st.success(f"Uploaded product in {elapsed_time:.2f} seconds!")
        return response.json()["job_id"]
    
    def upload_company_license(self, st_uploaded_file):
        st.info("Uploading company license...")
        start_time = time.time()

        url = f"{self.base_url}/company/upload"
        files = {
            "file": (st_uploaded_file.name, st_uploaded_file.getvalue(), st_uploaded_file.type)
        }
        response = requests.post(url, auth=self.auth, files=files)
        if response.status_code != 200:
            error_msg = f"Failed to upload company license: {response.text}"
            st.error(error_msg)
            raise Exception(error_msg)

        elapsed_time = time.time() - start_time
        st.success(f"Uploaded company license in {elapsed_time:.2f} seconds!")
        return response.json()["job_id"]
    
    def verify_company(self, product_job_id: str, product_filename: str, company_job_id: str):
        status_placeholder = st.empty()
        with status_placeholder:
            st.info("Verifying company license...")
        start_time = time.time()

        url = f"{self.base_url}/company/verify"
        response = requests.post(url, auth=self.auth, json={"product_job_id": product_job_id, "product_filename": product_filename, "company_job_id": company_job_id})
        if response.status_code != 200:
            error_msg = f"Failed to verify company license: {response.text}"
            st.error(error_msg)
            raise Exception(error_msg)

        elapsed_time = time.time() - start_time
        with status_placeholder:
            st.empty()
        st.info(f"Verified company license in {elapsed_time:.2f} seconds!")
        return response.json()["verification"]
    
    def verify_lab(self, job_id, filename):
        status_placeholder = st.empty()
        with status_placeholder:
            st.info("Verifying lab...")
        start_time = time.time()

        url = f"{self.base_url}/lab/verify"
        response = requests.post(url, auth=self.auth, json={"job_id": job_id, "filename": filename})
        if response.status_code != 200:
            error_msg = f"Failed to verify lab: {response.text}"
            st.error(error_msg)
            raise Exception(error_msg)

        elapsed_time = time.time() - start_time
        with status_placeholder:
            st.empty()
        st.info(f"Verified lab in {elapsed_time:.2f} seconds!")
        return response.json()["verification"]


    def verify_product_category(self, job_id, filename):
        status_placeholder = st.empty()
        with status_placeholder:
            st.info("Verifying product category...")
        start_time = time.time()

        url = f"{self.base_url}/product/verification/product-category"
        response = requests.post(url, auth=self.auth, json={"job_id": job_id, "filename": filename})
        if response.status_code != 200:
            error_msg = f"Failed to verify product category: {response.text}"
            st.error(error_msg)
            raise Exception(error_msg)

        elapsed_time = time.time() - start_time
        with status_placeholder:
            st.empty()
        st.info(f"Verified product category in {elapsed_time:.2f} seconds!")
        return response.json()["verification"]

    def verify_model_number(self, job_id, filename):
        status_placeholder = st.empty()
        with status_placeholder:
            st.info("Verifying model number...")
        start_time = time.time()

        url = f"{self.base_url}/product/verification/model-number"
        response = requests.post(url, auth=self.auth, json={"job_id": job_id, "filename": filename})
        if response.status_code != 200:
            error_msg = f"Failed to verify model number: {response.text}"
            st.error(error_msg)
            raise Exception(error_msg)

        elapsed_time = time.time() - start_time
        with status_placeholder:
            st.empty()
        st.info(f"Verified model number in {elapsed_time:.2f} seconds!")
        return response.json()["verification"]

    def verify_product_usage(self, job_id, filename):
        status_placeholder = st.empty()
        with status_placeholder:
            st.info("Verifying product usage...")
        start_time = time.time()

        url = f"{self.base_url}/product/verification/product-usage"
        response = requests.post(url, auth=self.auth, json={"job_id": job_id, "filename": filename})
        if response.status_code != 200:
            error_msg = f"Failed to verify product usage: {response.text}"
            st.error(error_msg)
            raise Exception(error_msg)

        elapsed_time = time.time() - start_time
        with status_placeholder:
            st.empty()
        st.info(f"Verified product usage in {elapsed_time:.2f} seconds!")
        return response.json()["verification"]

    def retrieve_certificate(self, job_id, filename):
        status_placeholder = st.empty()
        with status_placeholder:
            st.info("Retrieving certificate and extraction information...")
        start_time = time.time()

        url = f"{self.base_url}/certificate/retrieve"
        response = requests.post(url, auth=self.auth, json={"job_id": job_id, "filename": filename})
        if response.status_code != 200:
            error_msg = f"Failed to retrieve certificate: {response.text}"
            st.error(error_msg)
            raise Exception(error_msg)

        elapsed_time = time.time() - start_time
        with status_placeholder:
            st.empty()
        st.info(f"Retrieved certificate in {elapsed_time:.2f} seconds!")
        return response.json()["certificate"]

    def verify_certificate_manufacturer(self, certificate, job_id, filename):
        status_placeholder = st.empty()
        with status_placeholder:
            st.info("Verifying certificate manufacturer...")
        start_time = time.time()

        url = f"{self.base_url}/certificate/verification/manufacturer"
        response = requests.post(url, auth=self.auth, json={"certificate": certificate, "job_id": job_id, "filename": filename})
        if response.status_code != 200:
            error_msg = f"Failed to verify certificate manufacturer: {response.text}"
            st.error(error_msg)
            raise Exception(error_msg)

        elapsed_time = time.time() - start_time
        with status_placeholder:
            st.empty()
        st.info(f"Verified certificate manufacturer in {elapsed_time:.2f} seconds!")
        return response.json()["verification"]
    
    def verify_certificate_model_number(self, certificate, job_id, filename):
        status_placeholder = st.empty()
        with status_placeholder:
            st.info("Verifying certificate model number...")
        start_time = time.time()

        url = f"{self.base_url}/certificate/verification/model-number"
        response = requests.post(url, auth=self.auth, json={"certificate": certificate, "job_id": job_id, "filename": filename})
        if response.status_code != 200:
            error_msg = f"Failed to verify certificate model number: {response.text}"
            st.error(error_msg)
            raise Exception(error_msg)

        elapsed_time = time.time() - start_time
        with status_placeholder:
            st.empty()
        st.info(f"Verified model number on certificate in {elapsed_time:.2f} seconds!")
        return response.json()["verification"]
    
    def enhance_product_description(self, job_id, filename):
        status_placeholder = st.empty()
        with status_placeholder:
            st.info("Enhancing product description...")
        start_time = time.time()

        url = f"{self.base_url}/product/enhancement/product-description"
        response = requests.post(url, auth=self.auth, json={"job_id": job_id, "filename": filename})
        if response.status_code != 200:
            error_msg = f"Failed to enhance product description: {response.text}"
            st.error(error_msg)
            raise Exception(error_msg)
        
        elapsed_time = time.time() - start_time
        with status_placeholder:
            st.empty()
        st.info(f"Enhanced product description in {elapsed_time:.2f} seconds!")
        return response.json()["enhancement"]
