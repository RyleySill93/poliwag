import React from 'react';
import {
  Box,
  Divider,
  Stack,
  Typography
} from '@mui/material';

import useModal from '../hooks/useModal';
import { Option } from '../@types/common';

import Select from './Select';
import Drawer from './Drawer';

export type Props = {
  label: string;
  value: string;
  options: Option[];
  onChange: (value: string) => void;
  helperText?: string;
  error?: string;
  placeholder?: string;
}

const DrawerSelect = ({
  label: selectLabel,
  value: selectValue,
  options,
  onChange,
  helperText,
  error,
  ...props
}: Props) => {
  const { isOpen, openModal, closeModal } = useModal();

  return (
    <>
      <Box onClick={() => openModal()}>
        <Select
          label={selectLabel}
          helperText={helperText}
          error={error}
          options={options}
          value={selectValue}
          sx={{ pointerEvents: 'none' }}
          {...props}
        />
      </Box>
      <Drawer
        open={isOpen}
        onClose={closeModal}
      >
        <Box pt={3} width="100%" px={3}>
          <Typography variant="h4">
            {selectLabel}
          </Typography>
          <Stack divider={<Divider />}>
            {
                options.map(({ label, value }) => (
                  <Box
                    sx={{
                      cursor: 'pointer'
                    }}
                    py={2}
                    onClick={() => {
                      onChange(value);
                      closeModal();
                    }}
                  >
                    <Typography variant="body2" color="textSecondary">
                      {label}
                    </Typography>
                  </Box>
                ))
            }
          </Stack>
        </Box>
      </Drawer>
    </>
  );
};

export default DrawerSelect;
