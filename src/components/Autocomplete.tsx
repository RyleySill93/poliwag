import React from 'react';
import { Autocomplete as MuiAutocomplete } from '@mui/lab';

import TextField from './TextField';
import { Option } from '../@types/common';

interface Props {
    label: string;
    options: Option[];
    onChange: (value: string) => void;
    value?: string;
    error?: string;
}

const Autocomplete = ({
  label,
  options,
  onChange,
  value,
  ...props
}: Props) => {
  const optionByValue: Record<string, Option> = {};
  options.forEach((option) => {
    optionByValue[option.value] = option;
  });

  return (
    <MuiAutocomplete
      disablePortal
      id={label}
      value={value ? optionByValue[value] : null}
      onChange={(e, selectedOption) => {
        // @ts-ignore
        onChange(selectedOption?.value);
      }}
      options={options}
      renderInput={(params) => <TextField {...params} label={label} />}
      {...props}
    />
  );
};

export default Autocomplete;
