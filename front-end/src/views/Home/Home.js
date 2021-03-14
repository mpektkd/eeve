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

import Parallax from "components/Parallax/Parallax.js";
// sections for this page
import HeaderLinks from "components/Header/HeaderLinks.js";
import SectionPills from "./Sections/SectionPills.js";
import SectionDownload from "./Sections/SectionDownload.js";
import styles from "assets/jss/material-kit-react/views/components.js";
import axiosInstance from "../../axiosApi";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";

const useStyles = makeStyles(styles);


export default function Components(props) {
  const classes = useStyles();
  const { ...rest } = props;

  return (
    <div>
      <Header
        brand="eevie"
        rightLinks={<HeaderLinks/>}
        fixed
        color="transparent"
        changeColorOnScroll={{
          height: 200,
          color: "white"
        }}
        {...rest}
      />
      <Parallax image={require("assets/img/mybg1.jpg")}>
        
      </Parallax>

      <div className={classNames(classes.main, classes.mainRaised)}>
        <GridContainer justify="center" align="center" alignItems="center">
          <GridItem>
            <SectionPills/>
          </GridItem>
          <GridItem>
            <SectionDownload/>
          </GridItem>
        </GridContainer>
        
      </div>
      <Footer />
    </div>
  );
}
