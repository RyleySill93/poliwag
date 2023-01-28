import React from 'react';
import { DesktopDatePicker as MuiDatepicker } from '@mui/lab';

import TextField from './TextField';

export interface Props {
    label: string;
    error?: boolean;
    helperText?: string;
    placeholder?: string;
    onChange: (value: string) => void;
    value: string;
}

const DatePicker = ({
  label,
  error,
  helperText,
  placeholder,
  onChange,
  value,
  ...props
}: Props) => (
  <MuiDatepicker
    {...props}
    value={value}
    onChange={(date) => {
      // @ts-ignore
      if (date instanceof Date && !Number.isNaN(date.valueOf())) {
        const dateString = date.toISOString().slice(0, 10);
        onChange(dateString);
      }
    }}
    inputFormat="MM/dd/yyyy"
    renderInput={(params) => (
      <TextField
        {...params}
        error={error}
        helperText={helperText}
        label={label}
        placeholder={placeholder}
      />
    )}
  />
);

export default DatePicker;
