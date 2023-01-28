import React from 'react';
import { FormikContextType } from 'formik';
import TextField, { TextFieldProps } from '../TextField';

type Props = TextFieldProps & {
  formik: FormikContextType<any>;
  name: string;
  TextFieldComponent?: React.ElementType;
}

const FormikTextField = ({
  formik,
  name,
  TextFieldComponent = TextField,
  ...props
}: Props) => (
  <TextFieldComponent
    {...props}
    name={name}
    value={formik.values[name]}
    onChange={formik.handleChange}
    error={formik.touched[name] && Boolean(formik.errors[name])}
    helperText={formik.touched[name] && formik.errors[name]}
  />
);

export default FormikTextField;
