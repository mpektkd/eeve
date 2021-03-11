import React, { useState } from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import InputAdornment from "@material-ui/core/InputAdornment";
import Icon from "@material-ui/core/Icon";
// @material-ui/icons
import Email from "@material-ui/icons/Email";
// core components
import Header from "components/Header/Header.js";
import Footer from "components/Footer/Footer.js";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import Button from "components/CustomButtons/Button.js";
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import CardHeader from "components/Card/CardHeader.js";
import CardFooter from "components/Card/CardFooter.js";
import CustomDropdown from "components/CustomDropdown/CustomDropdown.js";
import Car from '@material-ui/icons/DriveEta';
import { Link } from "react-router-dom";
import Grid from "@material-ui/core/Grid";


import styles from "assets/jss/material-kit-react/views/loginPage.js";
import styles2 from "assets/jss/material-kit-react/components/headerLinksStyle.js";

import axiosInstance from "../../axiosApi";


import {useForm} from "react-hook-form";
import TextField from "@material-ui/core/TextField";
import { ThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import { green } from '@material-ui/core/colors';
import { Redirect } from "react-router";
import { isPropertySignature } from "typescript";
import { SystemUpdate } from "@material-ui/icons";
import axios from 'axios';

const useStyles = makeStyles(styles);
const useStyles2 = makeStyles(styles2);

const theme = createMuiTheme({
  palette: {
    primary: green
  },
});


export default function LoginPage(props) {
  const [cardAnimaton, setCardAnimation] = useState("cardHidden");
  setTimeout(function() {
    setCardAnimation("");
  }, 700);
  const {register, handleSubmit} = useForm();
  const [loggedIn, setLoggedIn] = useState(false);
  const [authError, setAuthError] = useState(false);
  const classes = useStyles();
  const classes2 = useStyles();
  const { ...rest } = props;
  const usernameProps = ["kwstas"];
  
  var car = {}, carList = [];


  React.useLayoutEffect ( () => {
    const response = axios.get('http://snf-881285.vm.okeanos.grnet.gr:8000/evcharge/api/cars/')
      .then(res => {
        for (var i = 0; i <res.data.length; i++) {
          if (res.data[i].release_year)
            car.name = res.data[i].brandName + " " + res.data[i].model + " " + res.data[i].release_year
          else 
            car.name = res.data[i].brandName + " " + res.data[i].model

          car.id = res.data[i].id;
          carList.push(car)
          car = {}
        }        
      })
      .catch(error => {
        console.log(error)
      })
  });


  const onSubmit = (e) => {
    try {
      const response = axiosInstance.post('signup/', {
        username: e.username,
        password: e.password,
        first_name: e.firstName,
        last_name: e.lastName,
        email: e.email,
        car_id: localStorage.getItem("carForSignUp")        
      })
      .then(res => {
        console.log(res)
       })
       .catch(error => {
         console.log(error)
       })
    } catch (error) {
      throw error;
    }
  }
 
  function FormTextField (props) {
    return (
      <TextField
      margin="normal"
      inputRef={register}
      required
      fullWidth
      name= {props.name}
      label= {props.label}
      type= {props.type}
      id= {props.id}
      autoComplete= {props.autoComplete}
    />);
  }

  return (
    <div>
      {loggedIn && <Redirect to = {'/'}/>}
      <Header
        absolute
        color="success"
        brand="eevie"
        {...rest}
      />
      <div
        style={{
          backgroundColor: "#fcfcfc",
          backgroundSize: "cover",
          backgroundPosition: "top center"
        }}
      >
        <div className={classes.container}>
          <GridContainer justify="center" align="center" alignItems="center">
            <GridItem xs={12} sm={12} md={4}>
              <Card className={classes[cardAnimaton]}>
                <form className={classes.form} onSubmit={handleSubmit( onSubmit )}>
                  <CardHeader color="success" className={classes.cardHeader}>
                    <h4>Sign up</h4>
                    <div className={classes.socialLine}>
                      <Button
                        justIcon
                        href="#pablo"
                        target="_blank"
                        color="transparent"
                        onClick={e => e.preventDefault()}
                      >
                        <i className={"fab fa-twitter"} />
                      </Button>
                      <Button
                        justIcon
                        href="#pablo"
                        target="_blank"
                        color="transparent"
                        onClick={e => e.preventDefault()}
                      >
                        <i className={"fab fa-facebook"} />
                      </Button>
                      <Button
                        justIcon
                        href="#pablo"
                        target="_blank"
                        color="transparent"
                        onClick={e => e.preventDefault()}
                      >
                        <i className={"fab fa-google-plus-g"} />
                      </Button>
                    </div>
                  </CardHeader>
                  <CardBody>
                  <ThemeProvider theme = { theme }>
                    <FormTextField label = {"First name"} name = {"firstName"} id = {"firstName"} autoComplete = {"firstName"} type = {"username"}/>
                    <FormTextField label = {"Last name"} name = {"lastName"} id = {"lastName"} autoComplete = {"lastName"} type = {"username"}/>
                    <FormTextField label = {"Email"} name = {"email"} id = {"email"} autoComplete = {"email"} type = {"email"}/>
                    <FormTextField label = {"Username"} name = {"username"} id = {"username"} autoComplete = {"username"} type = {"username"}/>
                    <FormTextField label = {"Password"} name = {"password"} id = {"password"} autoComplete = {"password"} type = {"password"}/>
                    <FormTextField label = {"Confirm Password"} name = {"confirmPassword"} id = {"confirmPassword"} autoComplete = {"confirmPassword"} type = {"password"}/>
                    </ThemeProvider>
                    <GridItem>
                      <p>{" "}</p>
                    </GridItem>
                    <GridItem>
                      <p>{" "}</p>
                    </GridItem>
                    <CustomDropdown
                        dropDownCar = { true }
                        buttonText="Select Car"
                        buttonProps={{
                          color: "success"
                        }}
                        buttonIcon={ Car }
                        dropdownList={ carList }
                    />       
                  </CardBody>
                  <CardFooter className={classes.cardFooter}>
                    <Button
                    simple
                    size = "lg"
                    type="submit"
                    variant="contained"
                    color="success"
                  >
                    Sign Up
                  </Button>
                  </CardFooter>
                </form>
              </Card>
            </GridItem>
          </GridContainer>
        </div>
        <Footer blackFont />
      </div>
    </div>
  );
}