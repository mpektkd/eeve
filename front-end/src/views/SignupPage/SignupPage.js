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
import DialogTitle from '@material-ui/core/DialogTitle';
import Dialog from '@material-ui/core/Dialog';
import Alert from '@material-ui/lab/Alert';
import AlertTitle from '@material-ui/lab/Alert';

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
  const [usernameError, setUsernameError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);
  const [alertOpen, setAlertOpen] = useState(false);
  const [signUpSuccessful, setSignUpSuccessful] = useState(false);
  const [carList, setCarList] = useState([]);
  const [defaultText, setDefaultText] = useState({
    firstName: "",
    lastName: "",
    email: "",
    username: "",
    password: "",
    confirmPassowrd: ""
  });

  const classes = useStyles();
  const classes2 = useStyles();
  const { ...rest } = props;

  React.useLayoutEffect ( () => {
    const response = axios.get('https://snf-881285.vm.okeanos.grnet.gr/evcharge/api/cars/')
      .then(res => {
        console.log(res)
        var car = {}, tempCarList = [];
        for (var i = 0; i <res.data.length; i++) {
          if (res.data[i].release_year)
            car.name = res.data[i].brandName + " " + res.data[i].model + " " + res.data[i].release_year
          else 
            car.name = res.data[i].brandName + " " + res.data[i].model

          car.id = res.data[i].id;
          tempCarList.push(car)
          car = {}
        }      
        console.log(tempCarList)  
        setCarList(tempCarList)
      })
      .catch(error => {
        console.log(error)
      })
  }, []);


  const onSubmit = (e) => {
    if (e.password !== e.confirmPassword) {
      setPasswordError(true)
      setDefaultText(e);
      return;
    }
    if (!localStorage.getItem("carForSignUp")) {
      setAlertOpen(true)
      setDefaultText(e);
      return;
    }
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
          setUsernameError(false)
          setSignUpSuccessful(true)
          localStorage.removeItem("carForSignUp")
        })
        .catch(error => {
          setDefaultText(e);
          setPasswordError(false)
          setUsernameError(true)
        })
    } 
    catch (error) {
      throw error;
    }
  }
 
  function FormTextField (props) {
    if (!passwordError && !usernameError && props.name === "firstName") {
      return (
        <TextField
        margin="normal"
        inputRef={register}
        required
        fullWidth
        name= {props.name}
        label= {props.label}
        autoFocus
        type= {props.type}
        id= {props.id}
        autoComplete= {props.autoComplete}
        defaultValue = {defaultText.firstName}
      />
      );
    }
    else if (usernameError && props.name === "username") {
      return (
        <TextField
        error
        margin="normal"
        inputRef={register}
        required
        fullWidth
        name= {props.name}
        label= {props.label}
        type= {props.type}
        id= {props.id}
        autoComplete= {props.autoComplete}
        helperText =  { "Username already taken!" }
        defaultValue = {props.defaultValue}
      />
      );
    }
    else if (passwordError && (props.name === "password" || props.name === "confirmPassword")) {
      return (
        <TextField
        error
        margin="normal"
        inputRef={register}
        required
        fullWidth
        name= {props.name}
        label= {props.label}
        type= {props.type}
        id= {props.id}
        autoComplete= {props.autoComplete}
        helperText =  { "Passwords do not match!" }
        defaultValue = {props.defaultValue}
      />
      );
    }
    else {
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
      defaultValue = {props.defaultValue}
    />);
    }
  }

  const handleClose = () => {
    setAlertOpen(false)
  };
  return (
    <div>
      {signUpSuccessful && <Redirect to = {'/'}/>}
      {alertOpen && <Dialog onClose = { handleClose } open = { true }>
        <Alert severity="error">
          Please Select A Car!
        </Alert>
      </Dialog>}
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
                    <FormTextField defaultValue = { defaultText.firstName } label = {"First name"} name = {"firstName"} id = {"firstName"} autoComplete = {"firstName"} type = {"username"}/>
                    <FormTextField defaultValue = { defaultText.lastName } label = {"Last name"} name = {"lastName"} id = {"lastName"} autoComplete = {"lastName"} type = {"username"}/>
                    <FormTextField defaultValue = { defaultText.email } label = {"Email"} name = {"email"} id = {"email"} autoComplete = {"email"} type = {"email"}/>
                    <FormTextField defaultValue = { defaultText.username } label = {"Username"} name = {"username"} id = {"username"} autoComplete = {"username"} type = {"username"}/>
                    <FormTextField defaultValue = { defaultText.password } label = {"Password"} name = {"password"} id = {"password"} autoComplete = {"password"} type = {"password"}/>
                    <FormTextField defaultValue = { defaultText.password } label = {"Confirm Password"} name = {"confirmPassword"} id = {"confirmPassword"} autoComplete = {"confirmPassword"} type = {"password"}/>
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