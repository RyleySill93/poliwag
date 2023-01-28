// @ts-ignore
import normalize from './normalize';

const toSnakeCase = (object: any) => normalize(object, 'snake');

export default toSnakeCase;
