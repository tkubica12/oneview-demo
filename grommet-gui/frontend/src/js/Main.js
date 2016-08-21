import React, { Component } from 'react';

//import Anchor from 'grommet/components/Anchor';
import App from 'grommet/components/App';
import Box from 'grommet/components/Box';
//import Header from 'grommet/components/Header';
//import Title from 'grommet/components/Title';

//import { browserHistory } from 'react-router';

export default class Main extends Component {
  render () {
    return (
      <App centered={false}>

        <Box pad={{horizontal: 'medium'}}>
          {this.props.children}
        </Box>
      </App>
    );
  }
};
