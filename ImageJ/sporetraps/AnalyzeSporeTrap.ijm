// Open image stack from arguments if available
var closeWindow = false;
if (lengthOf(getArgument()) > 0) {
	// Open the virtual stack of images
	open(getArgument(), "virtual");
	closeWindow = true;
}

// Check for RGB image
if (bitDepth() > 8) {
    // Convert to grayscale
    run("8-bit");
}

// Invert colors - white bg + black ROIs
run("Invert LUTs");

// Subtract background from image stack
run("Subtract Background...", "rolling=10 light stack");

// Generate a binary image from our image stack
setThreshold(50, 255, "raw");
setOption("BlackBackground", false);
run("Convert to Mask", "background=Light");
run("Fill Holes", "stack");
// Try to separate blobs into individual chromophores
run("Watershed", "stack");
saveAs("tif", "sporetraps/images/" + File.getName(getTitle()));

// Generate ROIs
run("Set Measurements...", "area centroid perimeter fit shape feret's stack redirect=None decimal=3");
run("Analyze Particles...", "circularity=0.00-1.00 show=Overlay display exclude include add stack");
roiManager("Show None");
saveAs("Results", "sporetraps/results/" + File.getNameWithoutExtension(getTitle()) + ".csv");

// Close ImageJ window when running in batches
if (closeWindow) {
	run("Quit");
}
