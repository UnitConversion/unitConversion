/*
 * Values for magnets module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 * @created: Oct 8, 2014
 */

app.constant('algorithmId', [
	{name: "i2b", value:"i2b"},
	{name: "b2i", value:"b2i"},
	{name: "i2k", value: "i2k"},
	{name: "k2i", value: "k2i"},
	{name: "b2k", value: "b2k"},
	{name: "k2b", value: "k2b"}
]);

app.constant('algorithmType', [
	{name: "1", value:"Linear fitting"},
	{name: "2", value:"2nd generation polinomial fitting"},
	{name: "3", value:"Measurement data"}
]);

app.constant('unitTypes', [
	{name: "A", value:"A"},
	{name: "T", value:"T"},
	{name: "T-m", value:"T-m"}
]);