var htmlEditor = ace.edit("html");
htmlEditor.setTheme("ace/theme/cobalt");
htmlEditor.session.setMode("ace/mode/html");
htmlEditor.resize();
htmlEditor.setHighlightActiveLine(false);

var cssEditor = ace.edit("css");
cssEditor.setTheme("ace/theme/cobalt");
cssEditor.session.setMode("ace/mode/css");
cssEditor.resize();
cssEditor.setHighlightActiveLine(false);

var jsEditor = ace.edit("js");
jsEditor.setTheme("ace/theme/cobalt");
jsEditor.session.setMode("ace/mode/javascript");
jsEditor.resize();
jsEditor.setHighlightActiveLine(false);

function compiler() {
  var htmlValue = htmlEditor.getValue();
  var cssValue = cssEditor.getValue();
  var jsValue = jsEditor.getValue();
  var result = document.getElementById("result").contentWindow.document;

  result.open();
  result.writeln(
    "<style>" +
    cssValue +
    "</style>" +
    htmlValue +
    "<script>" +
    jsValue +
    "</script>"
  );
  result.close();
}

var allButtons = document.querySelectorAll("#button-wrapper button");
var allPanels = document.querySelectorAll("#ide-container .panel-wrapper");

function switchPanel(panelIndex) {
  switcher(panelIndex);
}

switchPanel(0);

function runEdit(panelIndex) {
  switcher(panelIndex);
  compiler();
}

function switcher(panelIndex) {
  allButtons.forEach(function (node) {
    node.style.background = "";
  });
  allButtons[panelIndex].style.background = "#002240";
  allPanels.forEach(function (node) {
    node.style.display = "none";
  });
  allPanels[panelIndex].style.display = "block";
}
