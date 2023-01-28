import _ from 'lodash';
import methods from 'case';
import isUuid from './isUuid';

const normalize = (obj: any, caseType: 'camel' | 'snake' = 'camel') => {
  let ret = obj;
  const method = methods[caseType];

  if (Array.isArray(obj)) {
    ret = [];
    let i = 0;

    while (i < obj.length) {
      ret.push(normalize(obj[i], caseType));
      ++i;
    }
  } else if (_.isPlainObject(obj)) {
    ret = {};
    // eslint-disable-next-line guard-for-in, no-restricted-syntax
    for (const k in obj) {
      const key = isUuid(k) ? k : method(k);
      ret[key] = normalize(obj[k], caseType);
    }
  }

  return ret;
};

export default normalize;
