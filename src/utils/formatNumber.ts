import { replace } from 'lodash';
import numeral from 'numeral';

// ----------------------------------------------------------------------

export function formattedToNumber(number: string) {
  return Number(number.replace(/,/g, ''));
}

export function fCurrency(number: string | number, decimalPlaces: number = 0) {
  return numeral(number).format('$0,0.'.concat('0'.repeat(decimalPlaces)));
}

export function fScaledPercent(number: number) {
  return numeral(number / 100).format('0.0%');
}

export function fPercent(number: number) {
  if (number === null) return 'N/A';
  return numeral(number).format('0.0%');
}

export function fNumber(number: string | number | null, format?: string) {
  if (number === null) return 'N/A';
  return numeral(number).format(format);
}

export function fFloorNumber(number: string | number) {
  if (number === null) return 'N/A';
  return numeral(Math.floor(Number(number))).format();
}

export function fCeilNumber(number: string | number) {
  if (number === null) return 'N/A';
  return numeral(Math.ceil(Number(number))).format();
}

export function fShortenNumber(number: string | number) {
  return replace(numeral(number).format('0.00a'), '.00', '');
}

export function fData(number: string | number) {
  return numeral(number).format('0.0 b');
}
