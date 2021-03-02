/*eslint-disable*/
import React from "react";
import DeleteIcon from "@material-ui/icons/Delete";
import IconButton from "@material-ui/core/IconButton";
// react components for routing our app without refresh
import { Link } from "react-router-dom";

// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import Tooltip from "@material-ui/core/Tooltip";

// @material-ui/icons
import { Apps, CloudDownload } from "@material-ui/icons";

// core components
import CustomDropdown from "components/CustomDropdown/CustomDropdown.js";
import Button from "components/CustomButtons/Button.js";

import styles from "assets/jss/material-kit-react/components/headerLinksStyle.js";

const useStyles = makeStyles(styles);

export default function HeaderLinks(props) {
  const classes = useStyles();
  const onClick = () => {
    localStorage.clear();
  }
  if (localStorage.getItem("isLoggedIn")) {
    console.log(localStorage.getItem("username"))
    return (
      <List className={classes.list}>
         <ListItem className={classes.listItem}>
          <Button
            href = "/"
            color="transparent"
            target="_self"
            className={classes.navLink}
          >
          Home
          </Button>
        </ListItem>
  
        <ListItem className={classes.listItem}>
          <Button
            href = "/profile-page"
            color="transparent"
            target="_self"
            className={classes.navLink}
          >
           { localStorage.getItem("username")}
          </Button>
        </ListItem>
  
        <ListItem className={classes.listItem}>
          <Button
            href = "/map"
            color="transparent"
            target="_self"
            className={classes.navLink}
          >
           Map
          </Button>
        </ListItem>
  
         <ListItem className={classes.listItem}>
          <CustomDropdown
            noLiPadding
            buttonText="Options"
            buttonProps={{
              className: classes.navLink,
              color: "transparent"
            }}
            buttonIcon={Apps}
            dropdownList={[
              <Link to="/" className={classes.dropdownLink} onClick = { onClick }>
                Logout
              </Link>,
              <a
                href="https://creativetimofficial.github.io/material-kit-react/#/documentation?ref=mkr-navbar"
                target="_blank"
                className={classes.dropdownLink}
              >
                Documentation
              </a>
            ]}
          />
        </ListItem> 
      </List>
    );
  }
  else {
  return (
    <List className={classes.list}>
       <ListItem className={classes.listItem}>
        <Button
          href = "/"
          color="transparent"
          target="_self"
          className={classes.navLink}
        >
        Home
        </Button>
      </ListItem>

      <ListItem className={classes.listItem}>
        <Button
          href = "/profile-page"
          color="transparent"
          target="_self"
          className={classes.navLink}
        >
         Profile
        </Button>
      </ListItem>

      <ListItem className={classes.listItem}>
        <Button
          href = "/map"
          color="transparent"
          target="_self"
          className={classes.navLink}
        >
         Map
        </Button>
      </ListItem>
      
      <ListItem className={classes.listItem}>
        <Button
          href = "/login-page"
          color="transparent"
          target="_self"
          className={classes.navLink}
        >
         Sign in
        </Button>
      </ListItem>

      <ListItem className={classes.listItem}>
        <Button
          href = "/signup-page"
          color="success"
          target="_self"
          className={classes.navLink}
        >
         Sign up
        </Button>
      </ListItem>
    </List>
  );}
}
