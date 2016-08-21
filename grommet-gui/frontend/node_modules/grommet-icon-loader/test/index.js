// (C) Copyright 2014-2015 Hewlett Packard Enterprise Development LP

// run other tests
import './deep-filter';

// test for index.js
import test from 'tape';
import sinon from 'sinon';
import loader from '../src/index';

let svgSourceBasic = `
<?xml version="1.0" encoding="utf-8"?>
<!-- Generator: Adobe Illustrator 17.1.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" id="XMLID_313_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 24 24" enable-background="new 0 0 24 24" xml:space="preserve">
<g id="add">
	<rect id="_x2E_svg_1_" x="0" fill="none" width="24" height="24"/>
	<path fill="none" stroke="#000000" stroke-width="2" stroke-miterlimit="10" d="M0,12h24 M12,24V0"/>
</g>
</svg>
`;

let svgTargetBasic = `
// (C) Copyright 2014-2015 Hewlett Packard Enterprise Development LP

import React, { Component, PropTypes } from 'react';
import classnames from 'classnames';
import FormattedMessage from 'grommet/components/FormattedMessage';
import CSSClassnames from 'grommet/utils/CSSClassnames';

const CLASS_ROOT = CSSClassnames.CONTROL_ICON;
const COLOR_INDEX = CSSClassnames.COLOR_INDEX;

export default class Icon extends Component {
	render () {
		const { a11yTitleId, className, colorIndex } = this.props;
    let { a11yTitle, size } = this.props;

	  const classes = classnames(
	    CLASS_ROOT,
	    \`\${CLASS_ROOT}-add\`,
	    className,
	    {
	      [\`\${CLASS_ROOT}--\${size}\`]: size,
	      [\`\${COLOR_INDEX}-\${colorIndex}\`]: colorIndex
	    }
	  );

	  a11yTitle = a11yTitle || <FormattedMessage id="add" defaultMessage="add" />;

	  return <svg version="1.1" viewBox="0 0 24 24" width="24px" height="24px" role="img" className={classes} aria-labelledby={a11yTitleId}><title id={a11yTitleId}>{a11yTitle}</title><g id="add"><rect id="_x2E_svg_1_" x="0" fill="none" width="24" height="24"/><path fill="none" stroke="#000000" strokeWidth="2" strokeMiterlimit="10" d="M0,12h24 M12,24V0"/></g></svg>;
	}
};

Icon.propTypes = {
  a11yTitle: PropTypes.string,
  a11yTitleId: PropTypes.string,
  colorIndex: PropTypes.string,
  size: PropTypes.oneOf(['small', 'medium', 'large', 'xlarge', 'huge'])
};

Icon.defaultProps = {
  a11yTitleId: 'add-title'
};

Icon.icon = true;

Icon.displayName = 'Add';

`;

test('test basic loader output', function(t) {
  t.plan(5);
  let loaderContext = {
    query: '?copyright=(C) Copyright 2014-2015 Hewlett Packard Enterprise Development LP',
    cacheable: sinon.spy(),
    addDependency: sinon.spy(),
    resourcePath: '/fake/path/add.svg',
    async: function() {
      return function(err, result) {
        t.ok(err === null, 'no compilation errors occurred');
        t.ok(result, 'result exists');
        t.equal(result.replace(/\n|\s/g, ''), svgTargetBasic.replace(/\n|\s/g, ''));
      };
    }
  };
  loader.apply(loaderContext, [svgSourceBasic]);
  t.ok(loaderContext.addDependency.called, 'loader adds dependency');
  t.ok(loaderContext.cacheable.called, 'loader cached');
});
