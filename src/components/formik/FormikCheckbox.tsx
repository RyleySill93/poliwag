import React from 'react';
import { FormikContextType } from 'formik';
import Checkbox, { Props as CheckboxProps } from '../Checkbox';

type Props = Omit<CheckboxProps, 'onChange' | 'value'> & {
  formik: FormikContextType<any>;
  name: string;
}

const FormikCheckbox = ({ formik, name, ...props }: Props) => (
  <Checkbox
    {...props}
    value={formik.values[name]}
    onChange={formik.handleChange}
    error={formik.touched[name] && Boolean(formik.errors[name])}
    // @ts-ignore
    helperText={formik.touched[name] && formik.errors[name]}
  />
);

export default FormikCheckbox;
