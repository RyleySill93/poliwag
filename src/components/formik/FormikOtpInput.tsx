import React from 'react';
import { FormikContextType } from 'formik';
import OtpInput from '../OtpInput';

type Props = {
  formik: FormikContextType<any>;
  name: string;
  id?: string;
}

const FormikOtpInput = ({
  formik, name, ...props
}: Props) => (
  <OtpInput
    {...props}
    name={name}
    value={formik.values[name]}
    onChange={(value: string) => formik.setFieldValue(name, value)}
    error={formik.touched[name] && Boolean(formik.errors[name])}
    helperText={formik.touched[name] && formik.errors[name]}
  />
);

export default FormikOtpInput;
