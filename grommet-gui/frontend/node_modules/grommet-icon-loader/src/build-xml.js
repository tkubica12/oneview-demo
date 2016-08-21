// (C) Copyright 2014-2015 Hewlett Packard Enterprise Development LP

import builder from 'xmlbuilder';

let xmldec = {
  version: '1.0',
  standalone: true,
  encoding: 'UTF-8'
};

let svgAttributes = {
  version: "1.1",
  viewBox: "0 0 24 24",
  width: "24px",
  height: "24px",
  role: "img",
  className: "{classes}"
};

function traverse(tags, root) {
  for(var i in tags) {
    let item = root.ele(tags[i]['#name'], tags[i]['$']);
    if (tags[i].$$) traverse(tags[i].$$, item);
  }
}

export default function(json, fileName, copyright, context) {

  if (json.svg.$.viewBox) {
    svgAttributes.viewBox = json.svg.$.viewBox;
  }

  svgAttributes['aria-labelledby'] = '{a11yTitleId}';

  var root = builder.create('svg', xmldec, null, {
    headless: true
  });

  Object.keys(svgAttributes).map(function(at) {
    root.att(at, svgAttributes[at]);
  });

  root.ele('title', {
    id: '{a11yTitleId}'
  }, '{a11yTitle}');

  // for (var i in json.svg.$) root.att(i, json.svg.$[i]);
  traverse(json.svg.$$, root);

  return {
    svg: root.end().replace(/"{/g, '{').replace(/}"/g, '}'),
    fileName: fileName,
    copyright: copyright ? '// ' + copyright : '',
    context: context || 'grommet/'
  };
}
