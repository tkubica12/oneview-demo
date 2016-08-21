# grommet-icon-loader

Load SVG icons inside Grommet environment.

[![Build Status](https://travis-ci.org/grommet/grommet-icon-loader.svg)](https://travis-ci.org/grommet/grommet-icon-loader)

### WORK IN PROGRESS

This loader has been implemented based on the awesome [react-svg-loader](https://github.com/boopathi/react-svg-loader)

## Usage

```js
module.exports = {
  loaders: [
    {
      test: /.*img\/icons.*\.svg$/,
      loader: 'babel!grommet-icon!svgo'
    }
  ]
}
```

### Output

For the example input: 'src/img/icons/github.svg'

```js
var React = require('react');
var IntlMixin = require('grommet/mixins/GrommetIntlMixin');

var Icon = React.createClass({

  propTypes: {
    a11yTitle: React.PropTypes.string,
    a11yTitleId: React.PropTypes.string
  },

  mixins: [IntlMixin],

  getDefaultProps: function () {
    return {
      a11yTitleId: 'github-title'
    };
  },

  render: function() {
    var className = 'grommetux-control-icon grommetux-control-icon-github';
    if (this.props.className) {
      className += ' ' + this.props.className;
    }

    var a11yTitle = this.getGrommetIntlMessage(
      typeof this.props.a11yTitle !== "undefined" ?
        this.props.a11yTitle : 'github');

    return (
      <svg className={className} width="48px" height="48px"
        viewBox="0 0 48 48" version="1.1" aria-labelledby={this.props.a11yTitleId}>
        <title id={this.props.a11yTitleId}>{a11yTitle}</title>
        ...
      </svg>
    );
  }

});

module.exports = Icon;
```

## Assumptions and Other gotchas

+ Root element is always `<svg>`
+ namespace-d attributes (`myns:something`) are stripped
+ Hyphenated attributes are converted to camelCase. Others are preserved as it is
+ `style` tags are ignored
+ `root`'s attributes are parsed and overridden by props
+ Only tags allowed by react are retrieved. Others are simply ignored
+ Order of the tags are maintained as it is
+ Width and Height are always 48px
+ `grommetux-control-icon grommetux-control-icon-$fileName` class is added and overrides existing classes.
+ Accessibility configuration is added to your svg. Title will be added even if you don't have that in your original svg, as follows:

  ```
    <svg ...>
      <title id="$fileName-title">$fileName</title>
    </svg>
  ```

`$fileName` is the current name of the file being parsed by the loader.

## LICENSE

MIT License - http://boopathi.mit-license.org
