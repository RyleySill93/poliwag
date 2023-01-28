import { format, formatDistanceToNow } from 'date-fns';

// ----------------------------------------------------------------------
export function fShortDate(date: string | number | Date) {
  if (!date) return 'N/A';
  return format(new Date(date), 'MMM d');
}

export function fDate(date: string | number | Date) {
  if (!date) return 'N/A';
  return format(new Date(date), 'MMMM dd, yyyy');
}

export function fDateTime(date: string | number | Date) {
  return format(new Date(date), 'dd MMM yyyy HH:mm');
}

export function fDateTimeSuffix(date: string | number | Date) {
  return format(new Date(date), 'dd/MM/yyyy hh:mm p');
}

export function fToNow(date: string | number | Date) {
  return formatDistanceToNow(new Date(date), {
    addSuffix: true
  });
}
