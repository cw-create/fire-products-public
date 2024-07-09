import os

import streamlit as st
from handlers.product_handlers import ProductHandler
from utils.loggers import logger_name, make_logger

logger = make_logger(logger_name())

logo_path = os.path.join(os.path.dirname(__file__), "public/scale-logo.svg")
st.set_page_config(
    page_title="Building Permits",
    page_icon=logo_path,
)
st.logo(logo_path)


def display_verification_result(header_placeholder, status_placeholder, header_text, result):
    valid = result.get("valid", False)
    if header_text == "Verified product usage":
        valid = False
    explanation = result.get("explanation", "No explanation provided.")

    with header_placeholder:
        st.header(header_text)
    if valid:
        status_placeholder.subheader("Status: :green[PASSED]")
        st.success(explanation)
    else:
        status_placeholder.subheader("Status: :red[FAILED]")
        st.error(explanation)


def display_enhancement_result(header_placeholder, status_placeholder, header_text, result):
    enhanced_value = result.get("enhanced_value", "No enhanced value provided.")
    explanation = result.get("explanation", "No explanation provided.")

    with header_placeholder:
        st.header(header_text)
    status_placeholder.subheader("Status: :green[COMPLETED]")
    st.success(f"**Ideal product description:** \n\n {enhanced_value}")
    st.info(explanation)


def main():
    st.title("Scale's Fire Product Approval")

    from utils.auth import check_form

    if not check_form():
        st.stop()

    if "job_id" not in st.session_state:
        st.session_state.job_id = None

    if "company_job_id" not in st.session_state:
        st.session_state.company_job_id = None

    if "verification_result" not in st.session_state:
        st.session_state.verification_result = None

    uploaded_file = st.file_uploader("Upload Product CSV", type=["csv"])
    uploaded_license = st.file_uploader("Upload Company License PDF", type=["pdf"])

    if st.button(":rocket: Validate", type="primary"):
        if not uploaded_file or not uploaded_license:
            st.error("Please upload both the product CSV and the company license PDF files")
            return

        product_handler = ProductHandler()

        try:
            # Upload company license
            company_job_id = product_handler.upload_company_license(uploaded_license)
            st.session_state.company_job_id = company_job_id

            # Upload product file
            job_id = product_handler.upload(uploaded_file)
            st.session_state.job_id = job_id

            st.divider()

            # Verify company license
            company_verify_header = st.empty()
            company_verify_status = st.empty()
            with company_verify_header:
                st.header("Verifying company license...")

            result = product_handler.verify_company(job_id, uploaded_file.name, company_job_id)
            display_verification_result(
                company_verify_header,
                company_verify_status,
                "Verified company license",
                result,
            )

            st.divider()

            # Verify lab
            lab_verify_header = st.empty()
            lab_verify_status = st.empty()
            with lab_verify_header:
                st.header("Verifying lab...")

            result = product_handler.verify_lab(job_id, uploaded_file.name)
            display_verification_result(
                lab_verify_header,
                lab_verify_status,
                "Verified lab",
                result,
            )

            st.divider()

            # Product Category Verification
            product_category_header = st.empty()
            product_category_status = st.empty()
            with product_category_header:
                st.header("Verifying product category...")

            result = product_handler.verify_product_category(job_id, uploaded_file.name)
            display_verification_result(
                product_category_header,
                product_category_status,
                "Verified product category",
                result,
            )

            st.divider()

            # Model Number Verification
            model_number_header = st.empty()
            model_number_status = st.empty()
            with model_number_header:
                st.header("Verifying model number...")

            result = product_handler.verify_model_number(job_id, uploaded_file.name)
            display_verification_result(
                model_number_header, model_number_status, "Verified model number", result
            )

            st.divider()

            # Product Usage Verification
            product_usage_header = st.empty()
            product_usage_status = st.empty()
            with product_usage_header:
                st.header("Verifying product usage...")

            result = product_handler.verify_product_usage(job_id, uploaded_file.name)
            display_verification_result(
                product_usage_header, product_usage_status, "Verified product usage", result
            )

            st.divider()

            # Retrieve Certificate
            certificate_retrieve_header = st.empty()
            certificate_retrieve_status = st.empty()
            with certificate_retrieve_header:
                st.header("Retrieving certificate...")

            certificate = product_handler.retrieve_certificate(job_id, uploaded_file.name)
            st.session_state.certificate = certificate
            st.success("Certificate retrieved successfully.")

            st.divider()

            # Verify manufacturer on certificate
            certificate_manufacturer_header = st.empty()
            certificate_manufacturer_status = st.empty()
            with certificate_manufacturer_header:
                st.header("Verifying manufacturer on certificate...")

            result = product_handler.verify_certificate_manufacturer(certificate, job_id, uploaded_file.name)
            display_verification_result(
                certificate_manufacturer_header, certificate_manufacturer_status, "Verified manufacturer on certificate", result
            )

            st.divider()

            # Verify model number on certificate
            certificate_model_number_header = st.empty()
            certificate_model_number_status = st.empty()
            with certificate_model_number_header:
                st.header("Verifying model number on certificate...")

            result = product_handler.verify_certificate_model_number(certificate, job_id, uploaded_file.name)
            display_verification_result(
                certificate_model_number_header, certificate_model_number_status, "Verified model number on certificate", result
            )

            st.divider()

            # Enhance Product Description
            enhance_product_description_header = st.empty()
            enhance_product_description_status = st.empty()
            with enhance_product_description_header:
                st.header("Enhancing product description...")

            result = product_handler.enhance_product_description(job_id, uploaded_file.name)
            display_enhancement_result(
                enhance_product_description_header,
                enhance_product_description_status,
                "Enhanced product description",
                result,
            )

        except Exception:
            logger.exception("Error during validation")
            st.error(
                "An error occurred during the validation process. Please check the logs for more details."
            )


if __name__ == "__main__":
    main()
