// Helper functions
// Get Element by ID
function $id(id) {
	return document.getElementById(id);
}

// Output Info
function MessageOutput(msg) {
	var m = $id("messages");
	m.innerHTML = msg + m.innerHTML;
}

function ReleaseFormOutput(msg) {
	var m = $id("")
}

// call initialization file
if (window.File && window.FileList && window.FileReader) {
	Init();
}

//
// initialize
function Init() {

	var fileselect = $id("fileselect"),
		filedrag = $id("filedrag"),
		submitbutton = $id("uploadsubmitbutton"),
		formExtension = $id("form-extension");

	// file select
	fileselect.addEventListener("change", FileSelectHandler, false);

	// is XHR2 available?
	var xhr = new XMLHttpRequest();
	if (xhr.upload) {
	
		// file drop
		filedrag.addEventListener("dragover", FileDragHover, false);
		filedrag.addEventListener("dragleave", FileDragHover, false);
		filedrag.addEventListener("drop", FileSelectHandler, false);
		filedrag.style.display = "block";
		
		// remove submit button
		submitbutton.style.display = "none";
	}
	formExtension.style.display = "none"
}
// file drag hover
function FileDragHover(e) {
	e.stopPropagation();
	e.preventDefault();
	e.target.className = (e.type == "dragover" ? "hover" : "");
}
// file selection
function FileSelectHandler(e) {

	// cancel event and hover styling
	FileDragHover(e);

	// fetch FileList object
	var files = e.target.files || e.dataTransfer.files;

	// process all File objects
	for (var i = 0, f; f = files[i]; i++) {
		ParseFile(f);
	}
}

function ParseFile(file) {
	if(file.type.indexOf("video") == 0) {
		var reader = new FileReader();
		reader.onload= function(e) {
			MessageOutput(
				"<p><strong>" + file.name + ":</strong></p>" +
				"<video width='400' height='225'><source type='video/mp4' src='" + e.target.result + "'></video>"
				);
		};
		reader.readAsDataURL(file);
		var formExtension = $id("form-extension");
		formExtension.style.display = "block";
	} else {
		MessageOutput(
			"<div>Please Upload a video file!</div>"
			)
	}
	
}