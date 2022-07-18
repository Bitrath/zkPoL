pragma circom 2.0.4;

// Bitify
template Num2Bits(n) {
    signal input in;
    signal output out[n];
    var lc1=0;

    var e2=1;
    for (var i = 0; i<n; i++) {
        out[i] <-- (in >> i) & 1;
        out[i] * (out[i] -1 ) === 0;
        lc1 += out[i] * e2;
        e2 = e2+e2;
    }

    lc1 === in;
}

template Bits2Num(n) {
    signal input in[n];
    signal output out;
    var lc1=0;

    var e2 = 1;
    for (var i = 0; i<n; i++) {
        lc1 += in[i] * e2;
        e2 = e2 + e2;
    }

    lc1 ==> out;
}

// Binary Sum 
function nbits(a) {
    var n = 1;
    var r = 0;
    while (n-1<a) {
        r++;
        n *= 2;
    }
    return r;
}

template BinSum(n, ops) {
    var nout = nbits((2**n -1)*ops);
    signal input in[ops][n];
    signal output out[nout];

    var lin = 0;
    var lout = 0;

    var k;
    var j;

    var e2;

    e2 = 1;
    for (k=0; k<n; k++) {
        for (j=0; j<ops; j++) {
            lin += in[j][k] * e2;
        }
        e2 = e2 + e2;
    }

    e2 = 1;
    for (k=0; k<nout; k++) {
        out[k] <-- (lin >> k) & 1;

        // Ensure out is binary
        out[k] * (out[k] - 1) === 0;

        lout += out[k] * e2;

        e2 = e2+e2;
    }

    // Ensure the sum;

    lin === lout;
}

// Comparators
template IsZero() {
    signal input in;
    signal output out;

    signal inv;

    inv <-- in!=0 ? 1/in : 0;

    out <== -in*inv +1;
    in*out === 0;
}

template IsEqual() {
    signal input in[2];
    signal output out;

    component isz = IsZero();

    in[1] - in[0] ==> isz.in;

    isz.out ==> out;
}

template ForceEqualIfEnabled() {
    signal input enabled;
    signal input in[2];

    component isz = IsZero();

    in[1] - in[0] ==> isz.in;

    (1 - isz.out)*enabled === 0;
}

template LessThan(n) {
    assert(n <= 252);
    signal input in[2];
    signal output out;

    component n2b = Num2Bits(n+1);

    n2b.in <== in[0]+ (1<<n) - in[1];

    out <== 1-n2b.out[n];
}

// N is the number of bits the input  have.
// The MSF is the sign bit.
template LessEqThan(n) {
    signal input in[2];
    signal output out;

    component lt = LessThan(n);

    lt.in[0] <== in[0];
    lt.in[1] <== in[1]+1;
    lt.out ==> out;
}

template GreaterThan(n) {
    signal input in[2];
    signal output out;

    component lt = LessThan(n);

    lt.in[0] <== in[1];
    lt.in[1] <== in[0];
    lt.out ==> out;
}

template GreaterEqThan(n) {
    signal input in[2];
    signal output out;

    component lt = LessThan(n);

    lt.in[0] <== in[1];
    lt.in[1] <== in[0]+1;
    lt.out ==> out;
}

// Tests
template Simple(){
    signal input point[2];
    signal input polygon[3][2];
    signal output result;

    component checkGE = GreaterEqThan(16);
    checkGE.in[0] <== point[0];
    checkGE.in[1] <== polygon[1][0];
    result <== checkGE.out;
    result === 1;
}

/*
- This circuit multiplies ( a[n] + b ) n times.
- n number: MUST be inferior to the maximum available from the Tau Ceremony runned to verify the proof.
*/
template Multiplier(n){
    // Signals
    signal input a;
    signal input b;
    signal output c;

    // Intermediate Signal
    signal int[n];

    // First multiplication with Constraint
    int[0] <== a * b;
    // Next n-1 multiplications
    for(var i = 1; i < n; i++){
        int[i] <== int[i-1] * b;
    }

    // Output Constraint
    c <== int[n-1];
}

/* 
- This circuit template checks that c is the mulptiplication of a and b
*/
template Multiplier2(){
    // Signals
    signal input a;
    signal input b;
    signal output out;

    // Constraints
    out <== a * b;
}

/* 
- Testing Point In Polygon Algorithm
*/
template PointInPolygonTest(n){
    // Signals
    signal input point[2];
    signal input polygon[n][2];
    signal output inside;

    // Intermediate Signals
    signal part1[n];
    signal part2[n];
    signal orientation[n];

    // Components
    component checkLEZ[n];

    // Variables 
    var sum = 0;

    // Cycle onto polygon to get Orientations with point
    for(var i = 0; i < n; i++){
        var j = i + 1;
        if(j == n){ // Last vertex, segment with first point.
            j = 0;
        } 
        // Get Orientation
        part1[i] <== (point[1] - polygon[i][1])*(polygon[j][0] - polygon[i][0]);
        part2[i] <== (point[0] - polygon[i][0])*(polygon[j][1] - polygon[i][1]);
        orientation[i] <== part1[i] - part2[i];
        // Check if orientation is GreaterEqual than Zero
        // 16 bit check
        checkLEZ[i] = LessEqThan(16);
        checkLEZ[i].in[0] <== orientation[i];
        checkLEZ[i].in[1] <== 0;
        sum += checkLEZ[i].out;  // 1, it is; 0, it is not.
    }
    // If SUM is equal to n -> point in inside
    inside <-- sum;
    inside === 3;
}