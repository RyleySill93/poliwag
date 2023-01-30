import { Theme } from '@mui/material/styles';

// ----------------------------------------------------------------------

export default function Input(theme: Theme) {
  return {
    MuiInputBase: {
      styleOverrides: {
        root: {
          '&.Mui-disabled': {
            '& svg': { color: theme.palette.text.disabled }
          },
        },
        input: {
          '&::placeholder': {
            opacity: 1,
            color: theme.palette.text.disabled
          },
        },
        formControl: {
          borderRadius: '9px !important',
        }
      }
    },
    MuiInput: {
      styleOverrides: {
        underline: {
          '&:before': {
            borderBottomColor: theme.palette.grey[500_56]
          }
        },
      }
    },
    MuiFilledInput: {
      styleOverrides: {
        root: {
          backgroundColor: theme.palette.grey[500_12],
          '&:hover': {
            backgroundColor: theme.palette.grey[500_16]
          },
          '&.Mui-focused': {
            backgroundColor: theme.palette.action.focus
          },
          '&.Mui-disabled': {
            backgroundColor: theme.palette.action.disabledBackground
          }
        },
        underline: {
          '&:before': {
            borderBottomColor: theme.palette.grey[500_56]
          }
        }
      }
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-notchedOutline': {
            borderColor: 'transparent',
            backgroundColor: theme.palette.grey[500_12],
            '&:hover': {
              borderColor: 'red !important'
            },
            transition: theme.transitions.create('borderColor', {
              easing: theme.transitions.easing.sharp,
              duration: theme.transitions.duration.leavingScreen
            }),
          },
          '&.Mui-disabled': {
            '& .MuiOutlinedInput-notchedOutline': {
              borderColor: theme.palette.action.disabledBackground
            }
          },
        },
        input: {
          padding: '10px 38px 10px 10px',
        }
      }
    },
  };
}
