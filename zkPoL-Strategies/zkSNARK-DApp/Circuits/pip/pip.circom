pragma circom 2.0.4;

/* Include Control Flow templates */
include "../Utils/utils.circom";

/* 
- Returns a custom and approximate point as infinity 
*/
function pointToInfinty(){
    return 10000000;
}

/* 
- Returns the number of Bits used to setup logic comparators 
*/
function bits(){
    return 32;
}

/* 
- Returns the greater between two numbers 
*/
function maxN(x, y){
    if(x >= y) return x;
    return y;
}

/* 
- Returns the lower between two numbers 
*/
function minN(x, y){
    if(x >= y) return y;
    return x;
}

template OnVertex(){
    signal input p[2];
    signal input vertex[2];
    signal output out;

    component check1 = IsEqual();
    check1.in[0] <== p[0];
    check1.in[1] <== vertex[0];

    component check2 = IsEqual();
    check2.in[0] <== p[1];
    check2.in[1] <== vertex[1];

    var checks = check1.out + check2.out;
    var result = 0;

    if(checks == 2) result = 1;
    out <-- result;
}

template OnSegment(){
    signal input p[2];
    signal input q[2];
    signal input r[2];
    signal output out;
    
    var a = 0;
    var b = 0;

    a = p[0];
    b = r[0];
    var max1 = maxN(a, b);
    var min1 = minN(a, b);

    a = p[1];
    b = r[1];
    var max2 = maxN(a, b);
    var min2 = minN(a, b);

    component firstCheck = LessEqThan(bits());
    firstCheck.in[0] <== q[0];
    firstCheck.in[1] <-- max1;

    component secondCheck = GreaterEqThan(bits());
    secondCheck.in[0] <== q[0];
    secondCheck.in[1] <-- min1;

    component thirdCheck = LessEqThan(bits());
    thirdCheck.in[0] <== q[1];
    thirdCheck.in[1] <-- max2;

    component fourthCheck = GreaterEqThan(bits());
    fourthCheck.in[0] <== q[1];
    fourthCheck.in[1] <-- min2;

    var checks = firstCheck.out + secondCheck.out + thirdCheck.out + fourthCheck.out;
    var result = 0;

    if(checks == 4) result = 1;

    out <-- result;
}

template Orientation(){
    signal input p[2];
    signal input q[2];
    signal input r[2];
    signal output out;

    signal partOne;
    signal partTwo;

    var result = 0;
    var exit = 0;

    partOne <== (q[1] - p[1]) * (r[0] - q[0]);
    partTwo <== (q[0] - p[0]) * (r[1] - q[1]);

    result = partOne - partTwo;
    if(result > 0) exit = 3; // clock-wise
    if(result < 0) exit = 5; // counterclock-wise
    // else is 0: collinear

    out <-- exit;
}

/*
This template takes as inputs 4 signals that represent a point in space. 
It checks if the segment (p1, q1) intersects with the segment (p2, q2).
Outputs: 0 -> It does not intersect
         1 -> It does intersect
*/
template Intersects(){
    signal input p1[2];
    signal input q1[2];
    signal input p2[2];
    signal input q2[2];
    signal output out;

    component o1 = Orientation();
    o1.p[0] <== p1[0];
    o1.p[1] <== p1[1];
    o1.q[0] <== q1[0];
    o1.q[1] <== q1[1];
    o1.r[0] <== p2[0];
    o1.r[1] <== p2[1];

    component o2 = Orientation();
    o2.p[0] <== p1[0];
    o2.p[1] <== p1[1];
    o2.q[0] <== q1[0];
    o2.q[1] <== q1[1];
    o2.r[0] <== q2[0];
    o2.r[1] <== q2[1];

    component o3 = Orientation();
    o3.p[0] <== p2[0];
    o3.p[1] <== p2[1];
    o3.q[0] <== q2[0];
    o3.q[1] <== q2[1];
    o3.r[0] <== p1[0];
    o3.r[1] <== p1[1];

    component o4 = Orientation();
    o4.p[0] <== p2[0];
    o4.p[1] <== p2[1];
    o4.q[0] <== q2[0];
    o4.q[1] <== q2[1];
    o4.r[0] <== q1[0];
    o4.r[1] <== q1[1];

    var check = 0;
    var result = 0;

    // General Case (o1 != o2)&(o3 != o4)
    component eq1 = IsEqual(); 
    eq1.in[0] <== o1.out;
    eq1.in[1] <== o2.out;

    component eq2 = IsEqual(); 
    eq2.in[0] <== o3.out;
    eq2.in[1] <== o4.out;

    check = eq1.out + eq2.out; 
    if(check == 0) result = 1;

    // Special Case 1: (o1 == 0)&(onSegment)
    component eq3 = IsEqual();
    eq3.in[0] <== o1.out;
    eq3.in[1] <== 0;

    component segmentCheck1 = OnSegment();
    segmentCheck1.p[0] <== p1[0];
    segmentCheck1.p[1] <== p1[1];
    segmentCheck1.q[0] <== p2[0];
    segmentCheck1.q[1] <== p2[1];
    segmentCheck1.r[0] <== q1[0];
    segmentCheck1.r[1] <== q1[1];

    check = eq3.out + segmentCheck1.out;
    if(check == 2) result = 1;

    // Special Case 2: (o2 == 0)&(onSegment)
    component eq4 = IsEqual();
    eq4.in[0] <== o2.out;
    eq4.in[1] <== 0;

    component segmentCheck2 = OnSegment();
    segmentCheck2.p[0] <== p1[0];
    segmentCheck2.p[1] <== p1[1];
    segmentCheck2.q[0] <== q2[0];
    segmentCheck2.q[1] <== q2[1];
    segmentCheck2.r[0] <== q1[0];
    segmentCheck2.r[1] <== q1[1];

    check = eq4.out + segmentCheck2.out;
    if(check == 2) result = 1;

    // Special Case 3: (o3 == 0)&(onSegment)
    component eq5 = IsEqual();
    eq5.in[0] <== o3.out;
    eq5.in[1] <== 0;

    component segmentCheck3 = OnSegment();
    segmentCheck3.p[0] <== p2[0];
    segmentCheck3.p[1] <== p2[1];
    segmentCheck3.q[0] <== p1[0];
    segmentCheck3.q[1] <== p1[1];
    segmentCheck3.r[0] <== q2[0];
    segmentCheck3.r[1] <== q2[1];

    check = eq5.out + segmentCheck3.out;
    if(check == 2) result = 1;

    // Special Case 4: (o4 == 0)&(onSegment)
    component eq6 = IsEqual();
    eq6.in[0] <== o4.out;
    eq6.in[1] <== 0;

    component segmentCheck4 = OnSegment();
    segmentCheck4.p[0] <== p2[0];
    segmentCheck4.p[1] <== p2[1];
    segmentCheck4.q[0] <== q1[0];
    segmentCheck4.q[1] <== q1[1];
    segmentCheck4.r[0] <== q2[0];
    segmentCheck4.r[1] <== q2[1];

    check = eq6.out + segmentCheck4.out;
    if(check == 2) result = 1;

    log(result);
    out <-- result;
}

/*
Main Template to compute a Witness. 
It takes as signals:
    - private: point in space (x, y)
    - public: polygon (n vertexes)
If and only if the point lies inside the polygon, the circuit will successfully compile a Witness.
*/
template PointInPolygon(n){
    // If it has more than two vertexes, it is a polygon
    assert(n >= 3);

    // Main signals of the circuit
    signal input point[2];
    signal input polygon[n][2];
    signal output inside;

    // Load a fixed point to infitinity into a variable
    var extreme = pointToInfinty();

    // Create an intermediate signal that is the key segment to run PIP 
    // such as: ([point.x, point.y], [extreme, point.y])
    signal segmentInfinite[2][2];
    segmentInfinite[0][0] <== point[0];
    segmentInfinite[0][1] <== point[1];
    segmentInfinite[1][0] <== extreme;
    segmentInfinite[1][1] <== point[1];

    /* Lists of components needed to run checks for each segmemt of the polygon:
    - insterectP: check if the segment intersects with the key one
    - collinearP: check if the secret point is collinear with the segment of the iteration.
    - segmentP: check if the secret point lies on the iterated segment.
    - vertexP: check if the secret point lies on one of the vertexes of the iterated segment.
    */
    component intersectP[n];
    component collinearP[n];
    component segmentP[n];
    component vertexP[n];

    // Variable that stores all of the component results.
    var sum = 0;

    // iterate through each segment of the polygon and check various situations in relation to the key segment.
    for(var i = 0; i < n; i++){
        var j = i + 1;
        if(j == n){
            j = 0; // At the last cycle, load first polygon vertex
        }
        intersectP[i] = Intersects();
        intersectP[i].p1[0] <== polygon[i][0];
        intersectP[i].p1[1] <== polygon[i][1];
        intersectP[i].q1[0] <== polygon[j][0];
        intersectP[i].q1[1] <== polygon[j][1];
        intersectP[i].p2[0] <== segmentInfinite[0][0];
        intersectP[i].p2[1] <== segmentInfinite[0][1];
        intersectP[i].q2[0] <== segmentInfinite[1][0];
        intersectP[i].q2[1] <== segmentInfinite[1][1];
        sum += intersectP[i].out;

        // Check if P collinear with current segment
        collinearP[i] = Orientation();
        collinearP[i].p[0] <== polygon[i][0];
        collinearP[i].p[1] <== polygon[i][1];
        collinearP[i].q[0] <== point[0];
        collinearP[i].q[1] <== point[1];
        collinearP[i].r[0] <== polygon[j][0];
        collinearP[i].r[1] <== polygon[j][1];

        segmentP[i] = OnSegment(); 
        segmentP[i].p[0] <== polygon[i][0];
        segmentP[i].p[1] <== polygon[i][1];
        segmentP[i].q[0] <== point[0];
        segmentP[i].q[1] <== point[1];
        segmentP[i].r[0] <== polygon[j][0];
        segmentP[i].r[1] <== polygon[j][1];

        var checkSegmentP = collinearP[i].out + segmentP[i].out;
        if(checkSegmentP == 1) sum += 1;
        //log(checkSegmentP);

        // Check if P is equal to vertex[i]
        vertexP[i] = OnVertex();
        vertexP[i].p[0] <== point[0];
        vertexP[i].p[1] <== point[1];
        vertexP[i].vertex[0] <== polygon[i][0];
        vertexP[i].vertex[1] <== polygon[i][1];

        var checkVertexP = vertexP[i].out;
        if(checkVertexP == 1) sum += 1;
        //log(checkVertexP);
    }
    log(sum);
    // ASSERT: sum is ODD, OK to compute PROOF
    inside <-- sum % 2;
    inside === 1;
}

component main{public[polygon]} = PointInPolygon(7);