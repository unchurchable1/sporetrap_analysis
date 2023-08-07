// Open image from arguments if available
var closeWindow = false;
if (lengthOf(getArgument()) > 0) {
	// Open the image
	open(getArgument());
	closeWindow = true;
}

// Check for RGB image
if (bitDepth() > 16) {
    // Convert to grayscale
    run("16-bit");
}

// Invert colors - white bg + black ROIs
run("Invert LUT");

// Subtract background from image stack
run("Subtract Background...", "rolling=10 light stack");

// Generate a binary image from our image stack
setOption("BlackBackground", false);
run("Convert to Mask", "method=Default background=Light");
run("Fill Holes", "stack");
// Try to separate blobs into individual chromophores
run("Watershed", "stack");
saveAs("tif", "sporetraps/images/" + getTitle());

// Generate ROIs
run("Set Measurements...", "area centroid perimeter fit shape feret's stack redirect=None decimal=3");
run("Analyze Particles...", "circularity=0.00-1.00 show=Overlay display exclude include add stack");
roiManager("Show None");
saveAs("Results", "sporetraps/results/Results_" + File.getNameWithoutExtension(getTitle()) + ".csv");

// Close ImageJ window when running in batches
if (closeWindow) {
	run("Quit");
}
