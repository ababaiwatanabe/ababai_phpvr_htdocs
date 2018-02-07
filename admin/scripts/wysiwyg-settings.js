/********************************************************************
 * openWYSIWYG settings file Copyright (c) 2006 openWebWare.com
 * Contact us at devs@openwebware.com
 * This copyright notice MUST stay intact for use.
 *
 * $Id: wysiwyg-settings.js,v 1.4 2007/01/22 23:05:57 xhaggi Exp $
 ********************************************************************/

/*
 * Full featured setup used the openImageLibrary addon
var full = new WYSIWYG.Settings();
//full.ImagesDir = "images/";
//full.PopupsDir = "popups/";
//full.CSSFile = "styles/wysiwyg.css";
full.Width = "85%"; 
full.Height = "250px";
// customize toolbar buttons
full.addToolbarElement("font", 3, 1); 
full.addToolbarElement("fontsize", 3, 2);
full.addToolbarElement("headings", 3, 3);
// openImageLibrary addon implementation
full.ImagePopupFile = "addons/imagelibrary/insert_image.php";
full.ImagePopupWidth = 600;
full.ImagePopupHeight = 245;
 */

/*
 * Small Setup Example
 */
var small = new WYSIWYG.Settings();
small.CSSFile = "wysiwyg.css";
small.Width = "750px";
small.Height = "400px";
//small.DefaultStyle = "font-family: Arial; font-size: 12px; background-color: #AA99AA";
small.DefaultStyle = "font-size: 12px";
small.Toolbar[0] = new Array("fontsize" , "bold" , "italic" , "underline" , "forecolor" , "backcolor", "createlink", "viewSource");
//small.Toolbar[0] = new Array("font", "fontsize", "bold", "italic", "underline", "insertimage", "viewSource"); // small setup for toolbar 1
small.Toolbar[1] = ""; // disable toolbar 2
small.StatusBarEnabled = false;

//WYSIWYG.attach('param2', small); // small setup