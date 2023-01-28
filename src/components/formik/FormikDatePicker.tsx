import React from 'react';
import { FormikContextType } from 'formik';
import DatePicker, { Props as DatePickerProps } from '../DatePicker';

type Props = Omit<DatePickerProps, 'onChange' | 'value'> & {
  formik: FormikContextType<any>;
  name: string;
}

const FormikDatePicker = ({ formik, name, ...props }: Props) => (
  <DatePicker
    {...props}
    value={formik.values[name]}
    onChange={(value) => {
      formik.setFieldValue(name, value);
    }}
    // @ts-ignore
    error={formik.touched[name] && Boolean(formik.errors[name])}
    // @ts-ignore
    helperText={formik.touched[name] && formik.errors[name]}
  />
);

export default FormikDatePicker;
