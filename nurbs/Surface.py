"""
    NURBS Python Package
    Licensed under MIT License
    Developed by Onur Rauf Bingol (c) 2016-2017
"""

import sys
import itertools
import nurbs.utilities as utils


class Surface(object):

    def __init__(self):
        self._mDegreeU = 0
        self._mDegreeV = 0
        self._mKnotVectorU = []
        self._mKnotVectorV = []
        self._mCtrlPts = []
        self._mCtrlPts2D = []  # in [u][v] format
        self._mCtrlPts_sizeU = 0  # columns
        self._mCtrlPts_sizeV = 0  # rows
        self._mWeights = []
        self._mDelta = 0.01
        self._mSurfPts = []

    @property
    def degree_u(self):
        """ Getter method for degree U.
        :return: degree of U
        """
        return self._mDegreeU

    @degree_u.setter
    def degree_u(self, value):
        """ Setter method for degree U.
        :param value: input degree
        """
        if value < 0:
            raise ValueError("Degree cannot be less than zero.")
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set degree u
        self._mDegreeU = value

    @property
    def degree_v(self):
        """ Getter method for degree V.
        :return: degree of V
        """
        return self._mDegreeV

    @degree_v.setter
    def degree_v(self, value):
        """ Setter method for degree V.
        :param value: input degree
        """
        if value < 0:
            raise ValueError("Degree cannot be less than zero.")
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set degree v
        self._mDegreeV = value

    @property
    def ctrlpts(self):
        """ Getter method for 1D array of control points.
        :return: A tuple containing (x, y, z) values of the control points
        """
        ret_list = []
        for pt in self._mCtrlPts:
            ret_list.append(tuple(pt))
        return tuple(ret_list)

    @ctrlpts.setter
    def ctrlpts(self, value):
        """ Setter method for 1D array of control points.
        :param value: input control points
        """
        # Clean up the surface and control points lists, if necessary
        self._reset_surface()
        self._reset_ctrlpts()

        # First check v-direction
        if len(value) < self._mDegreeV + 1:
            raise ValueError("Number of control points in v-direction should be at least degree + 1.")
        # Then, check u direction
        u_cnt = 0
        for u_coords in value:
            if len(u_coords) < self._mDegreeU + 1:
                raise ValueError("Number of control points in u-direction should be at least degree + 1.")
            u_cnt += 1
            for coord in u_coords:
                # Save the control points as a list of 3D coordinates
                if len(coord) < 0 or len(coord) > 3:
                    raise ValueError("Please input 3D coordinates")
                # Convert to list of floats
                coord_float = [float(c) for c in coord]
                self._mCtrlPts.append(coord_float)
        # Set u and v sizes
        self._mCtrlPts_sizeU = u_cnt
        self._mCtrlPts_sizeV = len(value)
        # Generate a 2D list of control points
        for i in range(0, self._mCtrlPts_sizeU):
            ctrlpts_v = []
            for j in range(0, self._mCtrlPts_sizeV):
                ctrlpts_v.append(self._mCtrlPts[j + (i * self._mCtrlPts_sizeV)])
            self._mCtrlPts2D.append(ctrlpts_v)
        # Automatically generate a weights vector of 1.0s in the size of ctrlpts array
        self._mWeights = [1.0] * self._mCtrlPts_sizeU * self._mCtrlPts_sizeV

    @property
    def ctrlpts2d(self):
        """ Getter method for 2D array of control points.
        This list is automatically generated by ctrlpts() or read_ctrlpts()
        :return: A 2D list of control points in [u][v] format
        """
        return self._mCtrlPts2D

    @property
    def weights(self):
        """ Getter method for 1D array of weights.
        :return: A tuple containing the weights vector
        """
        return tuple(self._mWeights)

    @weights.setter
    def weights(self, value):
        """ Setter method for 1D array of weights.
        ctrlpts() and read_ctrlpts() automatically generate a weights vector of 1.0s in the size of control points array
        :param value: input weights vector
        """
        if len(value) != self._mCtrlPts_sizeU * self._mCtrlPts_sizeV:
            raise ValueError("Size of the weight vector should be equal to size of control points.")
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set weights vector
        value_float = [float(w) for w in value]
        self._mWeights = value_float

    @property
    def knotvector_u(self):
        """ Getter method for knot vector U.
        :return: A tuple containing the knot vector U
        """
        return tuple(self._mKnotVectorU)

    @knotvector_u.setter
    def knotvector_u(self, value):
        """ Setter method for knot vector U.
        :param value: input knot vector
        """
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set knot vector u
        value_float = [float(kv) for kv in value]
        self._mKnotVectorU = utils.normalize_knotvector(value_float)

    @property
    def knotvector_v(self):
        """ Getter method for knot vector V.
        :return: A tuple containing the knot vector V
        """
        return tuple(self._mKnotVectorV)

    @knotvector_v.setter
    def knotvector_v(self, value):
        """ Setter method for knot vector V.
        :param value: input knot vector
        """
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set knot vector u
        value_float = [float(kv) for kv in value]
        self._mKnotVectorV = utils.normalize_knotvector(value_float)

    @property
    def delta(self):
        """ Getter method for surface point calculation delta.
        :return: the delta value used to generate surface points
        """
        return self._mDelta

    @delta.setter
    def delta(self, value):
        """ Setter method for surface point calculation delta.
        :param value: input delta
        """
        # Delta value for surface calculations should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface calculation delta should be between 0.0 and 1.0.")
        # Clean up the surface points lists, if necessary
        self._reset_surface()
        # Set a new delta value
        self._mDelta = float(value)

    @property
    def ctrlptsw(self):
        """ Getter method for 1D array of weighted control points.
        :return: A tuple containing (x*w, y*w, z*w, w) values of the control points
        """
        ret_list = []
        for c, w in itertools.product(self._mCtrlPts, self._mWeights):
            temp = (float(c[0]*w), float(c[1]*w), float(c[2]*w), w)
            ret_list.append(temp)
        return tuple(ret_list)

    @ctrlptsw.setter
    def ctrlptsw(self, value):
        """ Setter method for 1D array of weighted control points.
        :param value: input weighted control points
        """
        # Start with clean lists
        ctrlpts_uv = []
        weights_uv = []
        # Split the weights vector from the input list for v-direction
        for udir in value:
            ctrlpts_u = []
            weights_u = []
            for i, c in enumerate(udir):
                temp_list = [float(c[0]/c[3]), float(c[1]/c[3]), float(c[2]/c[3])]
                ctrlpts_u.append(temp_list)
                weights_u.append(float(c[3]))
            ctrlpts_uv.append(ctrlpts_u)
            weights_uv.append(weights_u)
        # Assign unzipped values to the class fields
        self._mCtrlPts = ctrlpts_uv
        self._mWeights = weights_uv

    @property
    def surfpts(self):
        """ Getter method for calculated surface points.
        :return: 1D array of calculated surface points
        """
        return self._mSurfPts

    # Cleans up the control points and the weights (private)
    def _reset_ctrlpts(self):
        if self._mCtrlPts:
            # Delete control points
            del self._mCtrlPts[:]
            del self._mCtrlPts2D[:]
            # Delete weight vector
            del self._mWeights[:]
            # Set the control point sizes to zero
            self._mCtrlPts_sizeU = 0
            self._mCtrlPts_sizeV = 0

    # Cleans the calculated surface points (private)
    def _reset_surface(self):
        if self._mSurfPts:
            # Delete the calculated surface points
            del self._mSurfPts[:]

    # Checks if the calculation operations are possible (private)
    def _check_variables(self):
        works = True
        # Check degree values
        if self._mDegreeU == 0 or self._mDegreeV == 0:
            works = False

        if not self._mCtrlPts:
            works = False

        if not self._mKnotVectorU or not self._mKnotVectorV:
            works = False

        if not works:
            raise ValueError("Some required parameters for calculations are not set.")

    # Reads control points from a text file
    def read_ctrlpts(self, filename=''):
        # Clean up the surface and control points lists, if necessary
        self._reset_ctrlpts()
        self._reset_surface()

        # Try reading the file
        try:
            # Open the file
            with open(filename, 'r') as fp:
                for line in fp:
                    # Remove whitespace
                    line = line.strip()
                    # Convert the string containing the coordinates into a list
                    control_point_row = line.split(';')
                    self._mCtrlPts_sizeV = 0
                    for cpr in control_point_row:
                        control_point = cpr.split(',')
                        # Create a temporary dictionary for appending coordinates into ctrlpts list
                        pt = [float(control_point[0]), float(control_point[1]), float(control_point[2])]
                        # Add control points to the global control point list
                        self._mCtrlPts.append(pt)
                        self._mCtrlPts_sizeV += 1
                    self._mCtrlPts_sizeU += 1
            # Generate a 2D list of control points
            for i in range(0, self._mCtrlPts_sizeU):
                ctrlpts_v = []
                for j in range(0, self._mCtrlPts_sizeV):
                    ctrlpts_v.append(self._mCtrlPts[j + (i * self._mCtrlPts_sizeV)])
                self._mCtrlPts2D.append(ctrlpts_v)
            # Generate a 1D list of weights
            self._mWeights = [1.0] * self._mCtrlPts_sizeU * self._mCtrlPts_sizeV
        except IOError:
            print('ERROR: Cannot open file ' + filename)
            sys.exit(1)

        # Reads control points and weights from a text file
    def read_ctrlptsw(self, filename=''):
        # Clean up the surface and control points lists, if necessary
        self._reset_ctrlpts()
        self._reset_surface()

        # Try reading the file
        try:
            # Open the file
            with open(filename, 'r') as fp:
                for line in fp:
                    # Remove whitespace
                    line = line.strip()
                    # Convert the string containing the coordinates into a list
                    control_point_row = line.split(';')
                    self._mCtrlPts_sizeV = 0
                    for cpr in control_point_row:
                        cpt = cpr.split(',')
                        # Create a temporary dictionary for appending coordinates into ctrlpts list
                        pt = [float(cpt[0])/float(cpt[3]), float(cpt[1])/float(cpt[3]), float(cpt[2])/float(cpt[3])]
                        self._mWeights.append(float(cpt[3]))
                        # Add control points to the global control point list
                        self._mCtrlPts.append(pt)
                        self._mCtrlPts_sizeV += 1
                    self._mCtrlPts_sizeU += 1
            # Generate a 2D list of control points
            for i in range(0, self._mCtrlPts_sizeU):
                ctrlpts_v = []
                for j in range(0, self._mCtrlPts_sizeV):
                    ctrlpts_v.append(self._mCtrlPts[j + (i * self._mCtrlPts_sizeV)])
                self._mCtrlPts2D.append(ctrlpts_v)
        except IOError:
            print('ERROR: Cannot open file ' + filename)
            sys.exit(1)

    # Evaluates the B-Spline surface
    def evaluate(self):
        # Check all parameters are set before calculations
        self._check_variables()
        # Clean up the surface points lists, if necessary
        self._reset_surface()

        # Algorithm A3.5
        for v in utils.frange(0, 1, self._mDelta):
            span_v = utils.find_span(self._mDegreeV, tuple(self._mKnotVectorV), self._mCtrlPts_sizeV, v)
            basis_v = utils.basis_functions(self._mDegreeV, tuple(self._mKnotVectorV), span_v, v)
            for u in utils.frange(0, 1, self._mDelta):
                span_u = utils.find_span(self._mDegreeU, tuple(self._mKnotVectorU), self._mCtrlPts_sizeU, u)
                basis_u = utils.basis_functions(self._mDegreeU, tuple(self._mKnotVectorU), span_u, u)
                idx_u = span_u - self._mDegreeU
                surfpt = [0.0, 0.0, 0.0]
                for l in range(0, self._mDegreeV+1):
                    temp = [0.0, 0.0, 0.0]
                    idx_v = span_v - self._mDegreeV + l
                    for k in range(0, self._mDegreeU+1):
                        temp[0] += (basis_u[k] * self._mCtrlPts2D[idx_u + k][idx_v][0])
                        temp[1] += (basis_u[k] * self._mCtrlPts2D[idx_u + k][idx_v][1])
                        temp[2] += (basis_u[k] * self._mCtrlPts2D[idx_u + k][idx_v][2])
                    surfpt[0] += (basis_v[l] * temp[0])
                    surfpt[1] += (basis_v[l] * temp[1])
                    surfpt[2] += (basis_v[l] * temp[2])
                self._mSurfPts.append(surfpt)

    # Evaluates the NURBS surface
    def evaluate_rational(self):
        # Check all parameters are set before calculations
        self._check_variables()
        # Clean up the surface points lists, if necessary
        self._reset_surface()

        # Prepare a 2D weighted control points array
        ctrlptsw = []
        cnt = 0
        c_u = 0
        while c_u < self._mCtrlPts_sizeU:
            ctrlptsw_v = []
            c_v = 0
            while c_v < self._mCtrlPts_sizeV:
                temp = [self._mCtrlPts[cnt][0] * self._mWeights[cnt],
                        self._mCtrlPts[cnt][1] * self._mWeights[cnt],
                        self._mCtrlPts[cnt][2] * self._mWeights[cnt],
                        self._mWeights[cnt]]
                ctrlptsw_v.append(temp)
                c_v += 1
                cnt += 1
            ctrlptsw.append(ctrlptsw_v)
            c_u += 1

        # Algorithm A4.3
        for v in utils.frange(0, 1, self._mDelta):
            span_v = utils.find_span(self._mDegreeV, tuple(self._mKnotVectorV), self._mCtrlPts_sizeV, v)
            basis_v = utils.basis_functions(self._mDegreeV, tuple(self._mKnotVectorV), span_v, v)
            for u in utils.frange(0, 1, self._mDelta):
                span_u = utils.find_span(self._mDegreeU, tuple(self._mKnotVectorU), self._mCtrlPts_sizeU, u)
                basis_u = utils.basis_functions(self._mDegreeU, tuple(self._mKnotVectorU), span_u, u)
                idx_u = span_u - self._mDegreeU
                surfptw = [0.0, 0.0, 0.0, 0.0]
                for l in range(0, self._mDegreeV+1):
                    temp = [0.0, 0.0, 0.0, 0.0]
                    idx_v = span_v - self._mDegreeV + l
                    for k in range(0, self._mDegreeU+1):
                        temp[0] += (basis_u[k] * ctrlptsw[idx_u + k][idx_v][0])
                        temp[1] += (basis_u[k] * ctrlptsw[idx_u + k][idx_v][1])
                        temp[2] += (basis_u[k] * ctrlptsw[idx_u + k][idx_v][2])
                        temp[3] += (basis_u[k] * ctrlptsw[idx_u + k][idx_v][3])
                    surfptw[0] += (basis_v[l] * temp[0])
                    surfptw[1] += (basis_v[l] * temp[1])
                    surfptw[2] += (basis_v[l] * temp[2])
                    surfptw[3] += (basis_v[l] * temp[3])
                # Divide by weight to obtain 3D surface points
                surfpt = [surfptw[0] / surfptw[3], surfptw[1] / surfptw[3], surfptw[2] / surfptw[3]]
                self._mSurfPts.append(surfpt)

    # Calculates n-th order surface derivatives at the given (u,v) parameter
    def derivatives(self, u=-1, v=-1, order=0):
        # Check all parameters are set before calculations
        self._check_variables()
        # Check u and v parameters are correct
        utils.check_uv(u, v)

        # Algorithm A3.6
        du = min(self._mDegreeU, order)
        dv = min(self._mDegreeV, order)

        SKL = [[[0.0 for x in range(3)] for y in range(dv+1)] for z in range(du+1)]

        span_u = utils.find_span(self._mDegreeU, tuple(self._mKnotVectorU), self._mCtrlPts_sizeU, u)
        bfunsders_u = utils.basis_functions_ders(self._mDegreeU, self._mKnotVectorU, span_u, u, du)
        span_v = utils.find_span(self._mDegreeV, tuple(self._mKnotVectorV), self._mCtrlPts_sizeV, v)
        bfunsders_v = utils.basis_functions_ders(self._mDegreeV, self._mKnotVectorV, span_v, v, dv)

        for k in range(0, du+1):
            temp = [[] for y in range(self._mDegreeV+1)]
            for s in range(0, self._mDegreeV+1):
                temp[s] = [0.0 for x in range(3)]
                for r in range(0, self._mDegreeU+1):
                    cu = span_u - self._mDegreeU + r
                    cv = span_v - self._mDegreeV + s
                    temp[s][0] += (bfunsders_u[k][r] * self._mCtrlPts2D[cu][cv][0])
                    temp[s][1] += (bfunsders_u[k][r] * self._mCtrlPts2D[cu][cv][1])
                    temp[s][2] += (bfunsders_u[k][r] * self._mCtrlPts2D[cu][cv][2])
            dd = min(order - k, dv)
            for l in range(0, dd+1):
                for s in range(0, self._mDegreeV+1):
                    SKL[k][l][0] += (bfunsders_v[l][s] * temp[s][0])
                    SKL[k][l][1] += (bfunsders_v[l][s] * temp[s][1])
                    SKL[k][l][2] += (bfunsders_v[l][s] * temp[s][2])

        return SKL

    # Calculates surface tangent at the given (u, v) parameter
    def tangent(self, u=-1, v=-1):
        # Tangent is the 1st derivative of the surface
        skl = self.derivatives(u, v, 1)

        # Doing this just for readability
        point = skl[0][0]
        der_u = skl[1][0]
        der_v = skl[0][1]

        # Return the list of tangents w.r.t. u and v
        return tuple(point), tuple(der_u), tuple(der_v)

    # Calculates surface normal at the given (u, v) parameter
    def normal(self, u=-1, v=-1, normalized=True):
        # Check u and v parameters are correct for normal calculations
        utils.check_uv(u, v, test_normal=True, delta=self._mDelta)

        # Take the 1st derivative of the surface
        skl = self.derivatives(u, v, 1)

        point = skl[0][0]
        der_u = skl[1][0]
        der_v = skl[0][1]

        vect1 = (der_u[0] - point[0],
                 der_u[1] - point[1],
                 der_u[2] - point[2])
        vect2 = (der_v[0] - point[0],
                 der_v[1] - point[1],
                 der_v[2] - point[2])

        normal = utils.cross_vector(vect1, vect2)

        if normalized:
            normal = utils.normalize_vector(tuple(normal))

        # Return the surface normal at the input u,v location
        return tuple(normal)
