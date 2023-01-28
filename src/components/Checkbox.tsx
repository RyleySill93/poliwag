import React from 'react';

import { Checkbox as MuiCheckbox, FormControlLabel, FormHelperText } from '@mui/material';

export interface Props {
    checked?: boolean,
    label?: React.ReactNode,
    labelProps?: Object,
    helperText?: string,
    onChange: (event: any) => void
}

const Checkbox = ({
  checked,
  label,
  labelProps,
  helperText,
  ...props
}: Props) => (
  <>
    <FormControlLabel
      control={(
        <MuiCheckbox
          {...props}
          checked={checked}
        />
        )}
      label={label}
      {...labelProps}
    />
    {
      helperText && (
        <FormHelperText error>
          {helperText}
        </FormHelperText>
      )
    }
  </>
);

export default Checkbox;
