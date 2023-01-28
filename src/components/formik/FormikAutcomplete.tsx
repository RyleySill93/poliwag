import React from 'react';
import { FormikContextType } from 'formik';

import { Option } from '../../@types/common';
import Autocomplete from '../Autocomplete';

type Props = {
  formik: FormikContextType<any>;
  name: string;
  label?: string;
  options: Option[];
}

const FormikAutocomplete = ({ formik, name, ...props }: Props) => (
  <Autocomplete
    {...props}
    value={formik.values[name]}
    onChange={(value) => formik.setFieldValue(name, value)}
    // @ts-ignore
    error={(formik.touched[name] && formik.errors[name]) || ''}
  />
);

export default FormikAutocomplete;
