import normalize from './normalize';

const toCamelCase = (object: any) => normalize(object, 'camel');

export default toCamelCase;
