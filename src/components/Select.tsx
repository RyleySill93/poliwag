import React from 'react';

import {
  Select as MuiSelect,
  FormHelperText,
  FormControl,
  Box,
  Typography,
} from '@mui/material';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles(() => ({
  formControl: {
    display: 'flex'
  }
}));

const Select = ({
  id,
  options,
  label: selectLabel,
  helperText,
  isRequired,
  error,
  onClick,
  ...props
}: any) => {
  const classes = useStyles();

  return (
    <Box onClick={onClick}>
      <Typography variant="body2" mb={1}>
        {selectLabel}
      </Typography>
      <FormControl required={isRequired} variant="outlined" className={classes.formControl} {...props}>
        <MuiSelect
          id={props.name}
          inputProps={{
            name: props.name,
            id,
          }}
          error={Boolean(error)}
          {...props}
        >
          <option>&nbsp;</option>
          {options.map(({
            label,
            value
          }: any) => <option key={value} value={value}>{label}</option>)}
        </MuiSelect>
        {
          helperText && (
            <FormHelperText>
              {helperText}
            </FormHelperText>
          )
        }
        {
        error && (
          <FormHelperText error>
            {error}
          </FormHelperText>
        )
      }
      </FormControl>
    </Box>
  );
};

export default Select;
