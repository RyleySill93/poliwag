# PdfFiller
Package to create pdf form templates and fill them with mapped values.
 
### Quickstart
#### Defining a Template
 ```
from ._pdffiller import PdfFormTemplate

class MyPdfTemplate(PdfFormTemplate):
    # Top
    first_name = PdfFormTextField()
    # This field isn't required
    middle_name = PdfFormTextField(required=False)
    last_name = PdfFormTextField()
    
    # The form field is called 'dob' on the pdf template 
    birthday = PdfFormTextField(form_repr='dob')
    
    # Checkbox with multiple choices
    gender = RadioFormField(choices=['MALE', 'FEMALE'])

    # Implement the following methods
    def get_pdf_template(self) -> str:
        """
        Return path to pdf template
        """
        return os.path.join(settings.BROKERAGE_TEMPLATE_DIR, 'credo_form_1003.pdf')
    
    # What should we call the file for writes?
    def get_pdf_file_name(self) -> str:
        return f'{self.borrower}-{datetime.date.today()}.pdf'


```
#### Fill the template
``` python
from ._pdffiller import PdfFiller
template = MyPdfTemplate(
    first_name='John',
    last_name='Doe',
    dob=datetime.Datetime(1991, 8, 23),
    gender='MALE',
)
pdff = PdfFiller(template)
pdff.write()
```

### TODO
- Create sections and allow for conditional logic/validation
- Support for "formula" field types
- get_pdf_template should be able to return a file object as well
- Constructing from database on the fly (user generated custom templates)
- Documentation