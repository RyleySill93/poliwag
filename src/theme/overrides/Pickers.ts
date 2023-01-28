import { alpha, Theme } from '@mui/material/styles';

// ----------------------------------------------------------------------

export default function Pickers(theme: Theme) {
  return {
    PrivatePickersPopper: {
      styleOverrides: {
        paper: {
          boxShadow: theme.customShadows.z24,
          // @ts-ignore
          borderRadius: theme.shape.borderRadiusMd
        }
      }
    },

    PrivatePicker: {
      styleOverrides: {
        root: {
          overflow: 'hidden',
          // @ts-ignore
          borderRadius: theme.shape.borderRadiusMd,
          '& .PrivatePickersToolbar-root': {
            color: theme.palette.common.white,
            backgroundColor: theme.palette.primary.main,
            '& .MuiTypography-root': {
              color: alpha(theme.palette.common.white, 0.72),
              '&.Mui-selected': {
                color: theme.palette.common.white
              }
            }
          },
          '& .MuiTab-root': {
            margin: 0,
            color: alpha(theme.palette.common.white, 0.72),
            '&.Mui-selected': {
              color: theme.palette.common.white
            }
          },
          '& .MuiTabs-indicator': {
            width: '160px !important',
            backgroundColor: theme.palette.primary.dark
          }
        },
        landscape: {
          border: `solid 1px ${theme.palette.divider}`
        }
      }
    },

    MuiDateRangePickerViewDesktop: {
      styleOverrides: {
        root: {
          border: `solid 1px ${theme.palette.divider}`,
          // @ts-ignore
          borderRadius: theme.shape.borderRadiusMd
        }
      }
    }
  };
}
