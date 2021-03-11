import React from "react";
import { Redirect } from "react-router";
// nodejs library that concatenates classes
import classNames from "classnames";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// @material-ui/icons
import AttachMoneyIcon from '@material-ui/icons/AttachMoney';
import EqualizerIcon from '@material-ui/icons/Equalizer';
import Palette from "@material-ui/icons/Palette";
import DriveEtaIcon from '@material-ui/icons/DriveEta';
import Favorite from "@material-ui/icons/Favorite";
// core components
import Header from "components/Header/Header.js";
import Footer from "components/Footer/Footer.js";
import Button from "components/CustomButtons/Button.js";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import HeaderLinks from "components/Header/HeaderLinks.js";
import NavPills from "components/NavPills/NavPills.js";
import Parallax from "components/Parallax/Parallax.js";

import profile from "assets/img/faces/christian.jpg";

import studio1 from "assets/img/examples/studio-1.jpg";
import studio2 from "assets/img/examples/studio-2.jpg";
import studio3 from "assets/img/examples/studio-3.jpg";
import studio4 from "assets/img/examples/studio-4.jpg";
import studio5 from "assets/img/examples/studio-5.jpg";
import work1 from "assets/img/examples/olu-eletu.jpg";
import work2 from "assets/img/examples/clem-onojeghuo.jpg";
import work3 from "assets/img/examples/cynthia-del-rio.jpg";
import work4 from "assets/img/examples/mariya-georgieva.jpg";
import work5 from "assets/img/examples/clem-onojegaw.jpg";
import Card from "components/Bill/Card.js";
import CardHeader from "components/Bill/CardHeader.js";
import CardIcon from "components/Bill/CardIcon.js";
import CardBody from "components/Bill/CardBody.js";
import CardFooter from "components/Bill/CardFooter.js";
import styles from "assets/jss/material-kit-react/views/profilePage.js";
import DateRange from "@material-ui/icons/DateRange";
import Table from "components/Table/Table.js";

import styles2 from "assets/jss/material-dashboard-react/views/dashboardStyle.js";

const useStyles = makeStyles(styles);
const useStyles2 = makeStyles(styles2);


export default function ProfilePage(props) {
  const classes = useStyles();
  const classes2 = useStyles2();
  const { ...rest } = props;
  const imageClasses = classNames(
    classes.imgRaised,
    classes.imgRoundedCircle,
    classes.imgFluid
  );
  const navImageClasses = classNames(classes.imgRounded, classes.imgGallery);
  const bill = {amount: "107.00", date: "Last 24 hours"}
  console.log(bill);

  function Bill(props) {
    return (<GridItem xs={12} sm={7} md={4}>
      <Card>
        <CardHeader color="success" stats icon>
          <CardIcon color="success">
            Click to pay
          </CardIcon>
          <p className={classes2.cardCategory}>Bill</p>
          <h3 className={classes2.cardTitle}>${props.props.amount}</h3>
        </CardHeader>
        <CardFooter stats>
          <div className={classes2.stats}>
            <DateRange />
            {props.props.date}
          </div>
        </CardFooter>
      </Card>
    </GridItem>);
  }

  return (
    <div>
      { !localStorage.getItem("isLoggedIn") && <Redirect to = "/login-page"/>}
      <Header
        color="transparent"
        brand="eevie"
        rightLinks={<HeaderLinks />}
        fixed
        changeColorOnScroll={{
          height: 200,
          color: "white"
        }}
        {...rest}
      />
      <Parallax small filter image={require("assets/img/mybgblur.jpg")} />
      <div className={classNames(classes.main, classes.mainRaised)}>
        <div>
          <div className={classes.container}>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={6}>
                <div className={classes.profile}>
                  <div>
                    <img src={profile} alt="..." className={imageClasses} />
                  </div>
                  <div className={classes.name}>
                    <h3 className={classes.title}> { localStorage.getItem("username") } </h3>
                  </div>
                </div>
              </GridItem>
            </GridContainer>
            <div className={classes.description}>
              <p>
               Personilised data{" "}
              </p>
            </div>
            <GridContainer justify="center">
              <GridItem xs={12} sm={12} md={8} className={classes.navWrapper}>
                <NavPills
                  alignCenter
                  color="success"
                  tabs={[
                    {
                      tabButton: "My bills",
                      tabIcon: AttachMoneyIcon,
                      tabContent: (
                        <GridContainer>
                        <Bill props = {bill}></Bill>
                        </GridContainer>
                      )
                    },
                    {
                      tabButton: "Statistics",
                      tabIcon: EqualizerIcon,
                      tabContent: (
                        <GridContainer justify="center">
                          <GridItem xs={12} sm={12} md={12}>
                            <Card>
                              <CardHeader color="success">
                                <h4 className={classes.cardTitleWhite}>Bill History</h4>
                              </CardHeader>
                              <CardBody>
                                <Table
                                  tableHeaderColor="success"
                                  tableHead={["Bill ID", "Date", "Amount", "Location"]}
                                  tableData={[
                                    ["1", "03/02/2021", "$36,738", "Thiva"],
                                    ["2", "05/02/2021", "$23,789", "Athens"],
                                    ["3", "06/02/2021", "$56,142", "Athens"],
                                    ["4", "10/02/2021", "$38,735", "Athens"]
                                  ]}
                                />
                              </CardBody>
                            </Card>
                          </GridItem>
                        </GridContainer>
                      )
                    },
                    {
                      tabButton: "My vehicles",
                      tabIcon: DriveEtaIcon,
                      tabContent: (
                        <GridContainer>
                          <GridItem xs={12} sm={12} md={4}>
                            <img
                              alt="..."
                              src={work4}
                              className={navImageClasses}
                            />
                            <img
                              alt="..."
                              src={studio3}
                              className={navImageClasses}
                            />
                          </GridItem>
                          <GridItem xs={12} sm={12} md={4}>
                            <img
                              alt="..."
                              src={work2}
                              className={navImageClasses}
                            />
                            <img
                              alt="..."
                              src={work1}
                              className={navImageClasses}
                            />
                            <img
                              alt="..."
                              src={studio1}
                              className={navImageClasses}
                            />
                          </GridItem>
                        </GridContainer>
                      )
                    }
                  ]}
                />
              </GridItem>
            </GridContainer>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
