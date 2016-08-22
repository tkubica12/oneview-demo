import React, { Component } from 'react';
import Heading from 'grommet/components/Heading';
import Paragraph from 'grommet/components/Paragraph';
import Section from 'grommet/components/Section';
import Meter from 'grommet/components/Meter';
import Button from 'grommet/components/Button';
import Box from 'grommet/components/Box';
//import Notification from 'grommet/components/Notification';
import Form from 'grommet/components/Form';
import FormField from 'grommet/components/FormField';
import 'whatwg-fetch';

export default class Dashboard extends Component {

  constructor () {
    super();

    this.getVolumes = this.getVolumes.bind(this);
    this.storeVolumes = this.storeVolumes.bind(this);

    this.state = {
      volumeCount: 0,
      volumeList: ["<ListItem>test</ListItem>", "<ListItem>test2</ListItem>"]
    };
  }

  createVolume() {
    console.log(JSON.stringify({
      "volume_name": volume_name.value
    }));
    var httpRequest;
    httpRequest = new XMLHttpRequest();
    console.log(window.location.hostname);
    var url = "http://" + window.location.hostname + ":3000/volume";

    httpRequest.onreadystatechange = function() {
      if (httpRequest.readyState === XMLHttpRequest.DONE) {
        console.log(httpRequest.status);
        if (httpRequest.status === 200) {
          console.log(JSON.parse(httpRequest.responseText).state);
        } else {
          console.log('There was a problem with the request.');
        }
      }
    };
    httpRequest.open('POST', url, true);
    httpRequest.send(JSON.stringify({
      "volume_name": volume_name.value
    }));
  };

  storeVolumes (httpRequest) {
    return function () {
      if (httpRequest.readyState === XMLHttpRequest.DONE) {
        console.log(httpRequest.status);
        if (httpRequest.status === 200) {
          var count = JSON.parse(httpRequest.responseText).count;
          this.setState({ volumeCount: count });
        } else {
          console.log('There was a problem with the request.');
        }
      }
    }.bind(this);
  };

  getVolumes () {
    var httpRequest;
    httpRequest = new XMLHttpRequest();

    var url = "http://" + window.location.hostname + ":3000/volumes";

    httpRequest.onreadystatechange = this.storeVolumes(httpRequest);
    httpRequest.open('GET', url, true);
    httpRequest.send();
  };

  componentDidMount () {
    window.setInterval(function () {
      this.getVolumes();
    }.bind(this), 2000);
  };

  render () {
    return (
      <Section primary={true}>
        <Heading tag="h2">Moje Synergy</Heading>
        <Paragraph>Vytvoř si svůj disk</Paragraph>
        <Form onSubmit={this.funkce}>
          <FormField label="Název disku" htmlFor="volume_name">
            <input id="volume_name" type="text" />
          </FormField>
          <Paragraph></Paragraph>
          <Button label="Vytvoř" onClick={this.createVolume}/>
        </Form>
        <Paragraph></Paragraph>
        <Box separator="top">
          <Box direction="row" justify="between" pad={{"between": "small"}}>
            <Paragraph>Naše storage obsahuje:</Paragraph>
          </Box>
          <Meter id="meter" type="circle" value={this.state.volumeCount} threshold={90} units="disků"/>
        </Box>
      </Section>
    );
  }
};
