import datetime
import decimal
import os
import io
from poliwag.common.utils import legal_strftime, format_money, format_boolean
from poliwag.common.pdf._pdffiller import (
    PdfFormTemplate,
    fields,
    PdfFormFiller,
)


_FINALIS_CUSTOMER_ID_FORM = 'finalis-customer-id-form-2022-8.pdf'
class FinalisCIFFormTemplate(PdfFormTemplate):
    customer_name = fields.TextFormField(form_repr="SELLER_NAME", required=True)
    email = fields.TextFormField(form_repr="EMAIL", required=True)
    birthday = fields.TextFormField(form_repr="BIRTHDAY", required=True)
    street_address = fields.TextFormField(form_repr="STREET_ADDRESS", required=True)
    state = fields.TextFormField(form_repr="STATE", required=True)
    zipcode = fields.TextFormField(form_repr="ZIPCODE", required=True)
    phone = fields.TextFormField(form_repr="PHONE", required=True)
    employment_status = fields.TextFormField(form_repr="EMPLOYMENT_STATUS", required=True)
    occupation = fields.TextFormField(form_repr="OCCUPATION", required=True)
    employer = fields.TextFormField(form_repr="EMPLOYER", required=True)
    gross_income_current_year = fields.TextFormField(form_repr="GROSS_INCOME_CURRENT_YEAR", required=True)
    gross_income_previous_year = fields.TextFormField(form_repr="GROSS_INCOME_PREVIOUS_YEAR", required=True)
    estimated_net_worth = fields.TextFormField(form_repr="ESTIMATED_NET_WORTH", required=True)
    is_associated_with_securities_industry = fields.TextFormField(form_repr="IS_ASSOCIATED_WITH_SECURITIES_INDUSTRY", required=True)
    is_public_company_controller = fields.TextFormField(form_repr="IS_PUBLIC_COMPANY_CONTROLLER", required=True)
    signature_date = fields.TextFormField(form_repr="SIGNATURE_DATE", required=False)
    signature = fields.TextFormField(form_repr="SELLER_SIGNATURE", required=False)

    # We might fields to fill out here in the future
    def get_pdf_template(self) -> str:
        """
        Return path to pdf template
        """
        # Relative directory storage
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'templates',
            _FINALIS_CUSTOMER_ID_FORM
        )

    def get_pdf_file_name(self) -> str:
        return f'finalis-customer-id-form-{datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")}.pdf'


class FinalisCIFFormBuilder:
    def build(
        self,
        customer_name: str,
        email: str,
        birthday: datetime.date,
        street_address: str,
        state: str,
        zipcode: str,
        phone: str,
        employment_status: str,
        occupation: str,
        employer: str,
        gross_income_current_year: decimal.Decimal,
        gross_income_previous_year: decimal.Decimal,
        estimated_net_worth: str,
        is_associated_with_securities_industry: bool,
        is_public_company_controller: bool,
        is_signed: bool,
    ) -> io.BytesIO:
        signature = customer_name if is_signed else None
        template = FinalisCIFFormTemplate(
            customer_name=customer_name,
            email=email,
            birthday=birthday,
            street_address=street_address,
            state=state,
            zipcode=zipcode,
            phone=phone,
            employment_status=employment_status,
            occupation=occupation,
            employer=employer,
            gross_income_current_year=format_money(gross_income_current_year),
            gross_income_previous_year=format_money(gross_income_previous_year),
            estimated_net_worth=estimated_net_worth,
            is_associated_with_securities_industry=format_boolean(is_associated_with_securities_industry),
            is_public_company_controller=format_boolean(is_public_company_controller),
            signature=signature,
            signature_date=legal_strftime(datetime.date.today()),
        )
        pdff = PdfFormFiller(template)
        pdff.fill()
        # Used for testing which will dump to local dir
        # pdff.write()

        buffer = pdff.write_to_buffer()
        return buffer
