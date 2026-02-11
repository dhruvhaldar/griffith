function plotGrowth(c, m, stressRange, aInitial, aFinal, geometryFactor) {
    // Generate data points for the plot
    // da/dN = C * (Delta K)^m
    // Delta K = Y * Delta Sigma * sqrt(pi * a)
    // We integrate to find N vs a, or just plot da/dN vs a.

    // The proposal says: "Figure 3: Crack Growth Curve (a vs. N)."
    // So we need to calculate N for various 'a' from aInitial to aFinal.

    const steps = 50;
    const aValues = [];
    const nValues = [];

    // We can't easily integrate analytically in JS for arbitrary m.
    // Let's do a simple numerical integration (Riemann sum)

    let currentN = 0;
    const deltaA = (aFinal - aInitial) / steps;

    aValues.push(aInitial);
    nValues.push(0);

    for (let i = 0; i < steps; i++) {
        const a = aInitial + i * deltaA;
        const deltaK = geometryFactor * stressRange * Math.sqrt(Math.PI * a);
        const da_dn = c * Math.pow(deltaK, m);

        // dN = da / (da/dN)
        const dN = deltaA / da_dn;
        currentN += dN;

        aValues.push(a + deltaA);
        nValues.push(currentN);
    }

    const trace = {
        x: nValues,
        y: aValues.map(a => a * 1000), // Convert to mm
        mode: 'lines',
        name: 'Crack Growth',
        line: {
            color: 'rgb(55, 128, 191)',
            width: 3
        }
    };

    const layout = {
        title: 'Fatigue Crack Growth (a vs. N)',
        xaxis: {
            title: 'Cycles (N)'
        },
        yaxis: {
            title: 'Crack Length a (mm)'
        }
    };

    Plotly.newPlot('fatigue-plot', [trace], layout);
}
