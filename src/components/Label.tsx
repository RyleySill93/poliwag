import React from 'react';
// material
import {
  alpha, Theme, useTheme, experimentalStyled as styled
} from '@mui/material/styles';
import { BoxProps } from '@mui/material';
// @types
import { ColorSchema } from '../@types/theme';

// ----------------------------------------------------------------------

type LabelColor = 'default' | 'primary' | 'secondary' | 'info' | 'success' | 'warning' | 'error';

type LabelVariant = 'filled' | 'outlined' | 'ghost';

const RootStyle = styled('span')(
  ({
    theme,
    styleProps
  }: {
    theme: Theme;
    styleProps: {
      color: LabelColor;
      variant: LabelVariant;
    };
  }) => {
    const isLight = theme.palette.mode === 'light';
    const { color, variant } = styleProps;

    const styleFilled = (_color: ColorSchema) => ({
      color: theme.palette[_color].contrastText,
      backgroundColor: theme.palette[_color].main
    });

    const styleOutlined = (_color: ColorSchema) => ({
      color: theme.palette[_color].main,
      backgroundColor: 'transparent',
      border: `1px solid ${theme.palette[_color].main}`
    });

    const styleGhost = (_color: ColorSchema) => ({
      color: theme.palette[_color][isLight ? 'dark' : 'light'],
      backgroundColor: alpha(theme.palette[_color].main, 0.16)
    });

    return {
      height: 22,
      lineHeight: 0,
      borderRadius: 8,
      cursor: 'default',
      alignItems: 'center',
      whiteSpace: 'nowrap',
      display: 'inline-flex',
      justifyContent: 'center',
      padding: theme.spacing(0, 1),
      color: theme.palette.grey[800],
      fontSize: theme.typography.pxToRem(12),
      fontFamily: theme.typography.fontFamily,
      backgroundColor: theme.palette.grey[300],
      fontWeight: theme.typography.fontWeightBold,

      ...(color !== 'default'
        ? {
          ...(variant === 'filled' && { ...styleFilled(color) }),
          ...(variant === 'outlined' && { ...styleOutlined(color) }),
          ...(variant === 'ghost' && { ...styleGhost(color) })
        }
        : {
          ...(variant === 'outlined' && {
            backgroundColor: 'transparent',
            color: theme.palette.text.primary,
            border: `1px solid ${theme.palette.grey[500_32]}`
          }),
          ...(variant === 'ghost' && {
            color: isLight ? theme.palette.text.secondary : theme.palette.common.white,
            backgroundColor: theme.palette.grey[500_16]
          })
        })
    };
  }
);

// ----------------------------------------------------------------------

interface LabelProps extends BoxProps {
  color?: LabelColor;
  variant?: LabelVariant;
}

export default function Label({
  color = 'default', variant = 'ghost', children, sx, ...props
}: LabelProps) {
  const theme = useTheme();

  return (
    // @ts-ignore
    <RootStyle styleProps={{ color, variant }} sx={sx} theme={theme} {...props}>
      {children}
    </RootStyle>
  );
}
