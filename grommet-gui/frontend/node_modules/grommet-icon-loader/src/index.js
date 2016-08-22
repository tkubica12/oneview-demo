// (C) Copyright 2014-2015 Hewlett Packard Enterprise Development LP

import xml2js from 'xml2js';
import path from 'path';
import loaderUtils from 'loader-utils';
import builder from './build-xml';
import filter from './deep-filter';
import {svgTags, svgAttrs} from './react-svg-elements';
import makeComponent from './make-component';
import camelCase from 'camel-case';

export default function(content) {

  this.cacheable && this.cacheable(true);
  this.addDependency(this.resourcePath);
  var query = loaderUtils.parseQuery(this.query);

  var fileName = path.basename(this.resourcePath).split('.')[0];

  let loaderContext = this;
  let callback = this.async();

  let parser = new xml2js.Parser({
    normalize: true,
    normalizeTags: true,
    explicitArray: true,
    explicitChildren: true,
    preserveChildrenOrder: true
  });

  parser.addListener('error', err => callback(err));

  parser.addListener('end', function(result) {
    let svg = result.svg;
    let allowedTags = svgTags.concat(['$', '$$', '#name']);
    let filtered = filter(result, function(value, key, parent, parentKey) {
      if ('number' === typeof key) {
        if (parentKey === '$$')
          return allowedTags.indexOf(value['#name']) > -1;
        return true;
      }
      if (parentKey === '$') {
        // if the attribute is a namespace attr, then ignore
        if (key.indexOf(':') > -1) return false;
        // convert hyphens to camelcase
        if (key.indexOf('-') > -1) return camelCase(key);
        return true;
      }
      return allowedTags.indexOf(key) > -1;
    });

    // pass things through the pipeline
    // everything is synchronous anyway,
    // but the promise chain gives us a neat way to
    // list a pipeline - a list of transformations to
    // be done on some initial data
    Promise
      .resolve(filtered)
      .then(data => builder(data, fileName, query.copyright, query.context))
      .then(makeComponent)
      .then(component => callback(null, component))
      .catch(err => callback(err));

  });

  parser.parseString(content.toString());

};

module.exports = exports['default'];
