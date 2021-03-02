import React from "react";
// nodejs library that concatenates classes
import classNames from "classnames";
// react components for routing our app without refresh
import { Link } from "react-router-dom";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
// core components
import Header from "components/Header/Header.js";
import Footer from "components/Footer/Footer.js";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import Button from "components/CustomButtons/Button.js";
import Parallax from "components/Parallax/Parallax.js";
// sections for this page
import HeaderLinks from "components/Header/HeaderLinks.js";
import SectionBasics from "./Sections/SectionBasics.js";
import SectionNavbars from "./Sections/SectionNavbars.js";
import SectionTabs from "./Sections/SectionTabs.js";
import SectionPills from "./Sections/SectionPills.js";
import SectionNotifications from "./Sections/SectionNotifications.js";
import SectionTypography from "./Sections/SectionTypography.js";
import SectionJavascript from "./Sections/SectionJavascript.js";
import SectionCarousel from "./Sections/SectionCarousel.js";
import SectionCompletedExamples from "./Sections/SectionCompletedExamples.js";
import SectionLogin from "./Sections/SectionLogin.js";
import SectionExamples from "./Sections/SectionExamples.js";
import SectionDownload from "./Sections/SectionDownload.js";

import styles from "assets/jss/material-kit-react/views/components.js";
import {
  withGoogleMap,
  withScriptjs,
  GoogleMap,
  Marker,
  InfoWindow
} from "react-google-maps";
import mapStyles from "./mapStyles";



const useStyles = makeStyles(styles);

function Map() {
    return (
      <GoogleMap
        defaultZoom={10}
        defaultCenter={{ lat: 45.4211, lng: -75.6903 }}
        defaultOptions={{ styles: mapStyles }}
      >
      </GoogleMap>
    );
  }

  const MapWrapped = withScriptjs(withGoogleMap(Map));

export default function Components(props) {
  const classes = useStyles();
  const { ...rest } = props;
  return (
    <div>
      <Header
        brand="eevie"
        rightLinks={<HeaderLinks />}
        fixed
        color="white"
        
        {...rest}
      />
 

      <div className={classNames(classes.main)}>
        <div style={{ width: "100vw", height: "100vh" }}>
      <MapWrapped
        googleMapURL={`https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=AIzaSyBGTgwWi7-D6Jumc7LHb47BKJp6dTWPwH4`}
        loadingElement={<div style={{ height: `100%` }} />}
        containerElement={<div style={{ height: `100%` }} />}
        mapElement={<div style={{ height: `100%` }} />}
      />
    </div>
      </div>
      <Footer />
    </div>
  );
}
