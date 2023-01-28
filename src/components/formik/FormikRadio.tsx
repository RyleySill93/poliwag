import React from 'react';
import { FormikContextType } from 'formik';
import Radio, { Props as RadioProps } from '../Radio';

interface Props extends Omit<RadioProps, 'onChange'> {
  formik: FormikContextType<any>;
  name: string;
}

const FormikRadio = ({ formik, ...props }: Props) => (
  <Radio
    {...props}
    onChange={(e, value) => formik.setFieldValue(props.name, value)}
  />
);

export default FormikRadio;
