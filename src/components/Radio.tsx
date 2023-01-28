import React from 'react';
import {
  FormControl, FormControlLabel, FormLabel, Radio as MuiRadio, RadioGroup, Stack
} from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { Option } from '../@types/common';

export type Props = {
    name?: string;
    label?: string;
    options: Option[];
    onChange: (event: React.ChangeEvent<HTMLInputElement>, value: string) => void;
    FormControlProps?: any;
    RadioGroupProps?: any;
    FormControlLabelProps?: any;
}

const Radio = ({
  name,
  label,
  options,
  onChange,
  FormControlProps,
  RadioGroupProps,
  FormControlLabelProps,
}: Props) => {
  const theme = useTheme();
  return (
    <FormControl
      {...FormControlProps}
      sx={{
        width: '100%',
        ...FormControlProps?.sx,

      }}
    >
      <FormLabel
        id={name}
        sx={{
          color: theme.palette.text.primary,
          '&.Mui-focused': {
            color: theme.palette.text.primary,
          },
          pb: 1,
        }}
      >
        {label}
      </FormLabel>
      <RadioGroup
        row
        aria-labelledby={name}
        name={name}
        onChange={onChange}
        {...RadioGroupProps}
      >
        <Stack spacing={1} direction="row" sx={{ width: '100%' }}>
          {
            options.map(({
              value,
              label: _label,
            }) => (
              <FormControlLabel
                sx={{
                  backgroundColor: theme.palette.grey[100],
                  p: 1,
                  border: `1px solid ${theme.palette.divider}`,
                  borderRadius: '14px',
                  flex: '1 1',
                  m: 0,
                }}
                id={value}
                key={value}
                value={value}
                label={_label}
                labelPlacement="bottom"
                control={<MuiRadio />}
                {...FormControlLabelProps}
              />
            ))
        }
        </Stack>
      </RadioGroup>
    </FormControl>
  );
};

export default Radio;
