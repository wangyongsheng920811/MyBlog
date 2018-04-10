/**
 * @license Copyright (c) 2003-2018, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '';
    // config.filebrowserUploadUrl = '/ckupload/';
    // config.filebrowserImageBrowseUrl = '/upload/';
    config.filebrowserUploadUrl = '/ckupload/';
    config.width = '100%';
	config.height = '500px';
	// config.toolbar = 'Basic';
    // config.toolbarCanCollapse = true;
    config.dialog_backgroundCoverColor = '#3a3a3a';
	config.skin = 'moono-lisa';
	config.resize_enabled = false;
	config.toolbar = 'Full';
	 config.toolbar_Full = [
       ['Source','-','-'],
       ['Cut','Copy','Paste','PasteText','-'],
       ['Undo','Redo','-','Find','Replace','-','RemoveFormat'],
       ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
        ['NumberedList','BulletedList','-','Outdent','Indent'],
        ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
        ['Link','Unlink','Anchor'],
       ['Image','Table','HorizontalRule','SpecialChar'],
        ['Styles','Format','Font','FontSize'],
        ['TextColor','BGColor']
    ];

};
