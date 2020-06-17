var samp = (function() {
	var WEBSAMP_PORT = 21013;
	var WEBSAMP_PATH = "/";
	var WEBSAMP_PREFIX = "samp.webhub.";
	var WEBSAMP_CLIENT_PREFIX = "";

	TYPE_STRING = "string";
	TYPE_LIST = "list";
	TYPE_MAP = "map";

	var heir = function(proto) {
		function F() {
		}
		;
		F.prototype = proto;
		return new F();
	};

	var getSampType = function(obj) {
		if (typeof obj === "string") {
			return TYPE_STRING;
		} else if (obj instanceof Array) {
			return TYPE_LIST;
		} else if (obj instanceof Object && obj !== null) {
			return TYPE_MAP;
		} else {
			throw new Error("Not legal SAMP object type: " + obj + "-> ["
					+ JSON.stringify(obj, null, 4) + "]");
		}
	};
	var getChildElements = function(el, childTagName) {
		var children = el.childNodes;
		var child;
		var childEls = [];
		var i;
		for (i = 0; i < children.length; i++) {
			child = children[i];
			if (child.nodeType === 1) { // Element
				if (childTagName && (child.tagName !== childTagName)) {
					throw new Error("Child <" + children[i].tagName + ">"
							+ " of <" + el.tagName + ">" + " is not a <"
							+ childTagName + ">");
				}
				childEls.push(child);
			}
		}
		return childEls;
	};
	var getSoleChild = function(el, childTagName) {
		var children = getChildElements(el, childTagName);
		if (children.length === 1) {
			return children[0];
		} else {
			throw new Error("No sole child of <" + el.tagName + ">");
		}
	};
	var getTextContent = function(el) {
		var txt = "";
		var i;
		var child;
		for (i = 0; i < el.childNodes.length; i++) {
			child = el.childNodes[i];
			if (child.nodeType === 1) { // Element
				throw new Error("Element found in text content");
			} else if (child.nodeType === 3 || // Text
			child.nodeType === 4) { // CDATASection
				txt += child.nodeValue;
			}
		}
		return txt;
	};
	var stringify = function(obj) {
		return typeof JSON === "undefined" ? "..." : JSON.stringify(obj);
	};

	var XmlRpc = {};
	XmlRpc.escapeXml = function(s) {
		return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g,
				"&gt;");
	};
	XmlRpc.checkParams = function(paramList, typeList) {
		var i;
		for (i = 0; i < typeList.length; i++) {
			if (typeList[i] !== TYPE_STRING && typeList[i] !== TYPE_LIST
					&& typeList[i] !== TYPE_MAP) {
				throw new Error("Unknown type " + typeList[i]
						+ " in check list");
			}
		}
		var npar = paramList.length;
		var actualTypeList = [];
		var ok = true;
		for (i = 0; i < npar; i++) {
			actualTypeList.push(getSampType(paramList[i]));
		}
		ok = ok && (typeList.length === npar);
		for (i = 0; ok && i < npar; i++) {
			ok = ok && typeList[i] === actualTypeList[i];
		}
		if (!ok) {
			throw new Error("Param type list mismatch: " + "[" + typeList
					+ "] != " + "[" + actualTypeList + "]");
		}
	};
	XmlRpc.valueToXml = function v2x(obj, prefix) {
		prefix = prefix || "";
		var a;
		var i;
		var result;
		var type = getSampType(obj);
		if (type === TYPE_STRING) {
			return prefix + "<value><string>" + XmlRpc.escapeXml(obj)
					+ "</string></value>";
		} else if (type === TYPE_LIST) {
			result = [];
			result.push(prefix + "<value>", prefix + "  <array>", prefix
					+ "    <data>");
			for (i = 0; i < obj.length; i++) {
				result.push(v2x(obj[i], prefix + "      "));
			}
			result.push(prefix + "    </data>", prefix + "  </array>", prefix
					+ "</value>");

			return result.join("\n");
		} else if (type === TYPE_MAP) {
			result = [];
			result.push(prefix + "<value>");
			result.push(prefix + "  <struct>");
			for (i in obj) {
				result.push(prefix + "    <member>");
				result.push(prefix + "      <name>" + XmlRpc.escapeXml(i)
						+ "</name>");
				result.push(v2x(obj[i], prefix + "      "));
				result.push(prefix + "    </member>");
			}
			result.push(prefix + "  </struct>");
			result.push(prefix + "</value>");
			return result.join("\n");
		} else {
			throw new Error("bad type"); // shouldn't get here
		}
	};
	XmlRpc.xmlToValue = function x2v(valueEl, allowInt) {
		var childEls = getChildElements(valueEl);
		var i;
		var j;
		var txt;
		var node;
		var childEl;
		var elName;
		if (childEls.length === 0) {
			return getTextContent(valueEl);
		} else if (childEls.length === 1) {
			childEl = childEls[0];
			elName = childEl.tagName;
			if (elName === "string") {
				return getTextContent(childEl);
			} else if (elName === "array") {
				var valueEls = getChildElements(getSoleChild(childEl, "data"),
						"value");
				var list = [];
				for (i = 0; i < valueEls.length; i++) {
					list.push(x2v(valueEls[i], allowInt));
				}
				return list;
			} else if (elName === "struct") {
				var memberEls = getChildElements(childEl, "member");
				var map = {};
				var s_name;
				var s_value;
				var jc;
				for (i = 0; i < memberEls.length; i++) {
					s_name = undefined;
					s_value = undefined;
					for (j = 0; j < memberEls[i].childNodes.length; j++) {
						jc = memberEls[i].childNodes[j];
						if (jc.nodeType == 1) {
							if (jc.tagName === "name") {
								s_name = getTextContent(jc);
							} else if (jc.tagName === "value") {
								s_value = x2v(jc, allowInt);
							}
						}
					}
					if (s_name !== undefined && s_value !== undefined) {
						map[s_name] = s_value;
					} else {
						throw new Error("No <name> and/or <value> "
								+ "in <member>?");
					}
				}
				return map;
			} else if (allowInt && (elName === "int" || elName === "i4")) {
				return getTextContent(childEl);
			} else {
				throw new Error("Non SAMP-friendly value content: " + "<"
						+ elName + ">");
			}
		} else {
			throw new Error("Bad XML-RPC <value> content - multiple elements");
		}
	};
	XmlRpc.decodeParams = function(paramsEl) {
		var paramEls = getChildElements(paramsEl, "param");
		var i;
		var results = [];
		for (i = 0; i < paramEls.length; i++) {
			results.push(XmlRpc.xmlToValue(getSoleChild(paramEls[i], "value")));
		}
		return results;
	};
	XmlRpc.decodeFault = function(faultEl) {
		var faultObj = XmlRpc.xmlToValue(getSoleChild(faultEl, "value"), true);
		return new XmlRpc.Fault(faultObj.faultString, faultObj.faultCode);
	};
	XmlRpc.decodeResponse = function(xml) {
		var mrEl = xml.documentElement;
		if (mrEl.tagName !== "methodResponse") {
			throw new Error("Response element is not <methodResponse>");
		}
		var contentEl = getSoleChild(mrEl);
		if (contentEl.tagName === "fault") {
			return XmlRpc.decodeFault(contentEl);
		} else if (contentEl.tagName === "params") {
			return XmlRpc.decodeParams(contentEl)[0];
		} else {
			throw new Error("Bad XML-RPC response - unknown element" + " <"
					+ contentEl.tagName + ">");
		}
	};
	XmlRpc.Fault = function(faultString, faultCode) {
		this.faultString = faultString;
		this.faultCode = faultCode;
	};
	XmlRpc.Fault.prototype.toString = function() {
		return "XML-RPC Fault (" + this.faultCode + "): " + this.faultString;
	};

	var XmlRpcRequest = function(methodName, params) {
		this.methodName = methodName;
		this.params = params || [];
	}
	XmlRpcRequest.prototype.toString = function() {
		return this.methodName + "(" + stringify(this.params) + ")";
	};
	XmlRpcRequest.prototype.addParam = function(param) {
		this.params.push(param);
		return this;
	};
	XmlRpcRequest.prototype.addParams = function(params) {
		var i;
		for (i = 0; i < params.length; i++) {
			this.params.push(params[i]);
		}
		return this;
	};
	XmlRpcRequest.prototype.checkParams = function(typeList) {
		XmlRpc.checkParams(this.params, typeList);
	};
	XmlRpcRequest.prototype.toXml = function() {
		var lines = [];
		lines.push("<?xml version='1.0'?>", "<methodCall>", "  <methodName>"
				+ this.methodName + "</methodName>", "  <params>");
		for ( var i = 0; i < this.params.length; i++) {
			lines.push("    <param>", XmlRpc.valueToXml(this.params[i],
					"      "), "    </param>");
		}
		lines.push("  </params>", "</methodCall>");
		return lines.join("\n");
	};

	var XmlRpcClient = function(endpoint) {
		this.endpoint = endpoint || "http://localhost:" + WEBSAMP_PORT
				+ WEBSAMP_PATH;
	};
	XmlRpcClient.createXHR = function() {
		// interface:
		// open(method, url)
		// send(body)
		// abort()
		// setContentType()
		// responseText
		// responseXML
		// onload
		// onerror(err) - includes timeout; abort is ignored
		var XhrL2 = function(xhr) {
			this.xhr = xhr;
			xhr.onreadystatechange = (function(l2) {
				return function() {
					if (xhr.readyState !== 4) {
						return;
					} else if (!l2.completed) {
						l2.completed = true;
						if (+xhr.status === 200) {
							l2.responseText = xhr.responseText;
							l2.responseXML = xhr.responseXML;
							if (l2.onload) {
								l2.onload();
							}
						}
					}
				};
			})(this);
			xhr.onerror = (function(l2) {
				return function(event) {
					if (!l2.completed) {
						l2.completed = true;
						if (l2.onerror) {
							if (event) {
								event.toString = function() {
									return "No hub?";
								};
							} else {
								event = "No hub?";
							}
							l2.onerror(event);
						}
					}
				};
			})(this);
			xhr.ontimeout = (function(l2) {
				return function(event) {
					if (!l2.completed) {
						l2.completed = true;
						if (l2.onerror) {
							l2.onerror("timeout");
						}
					}
				};
			})(this);
		};
		XhrL2.prototype.open = function(method, url) {
			this.xhr.open(method, url);
		};
		XhrL2.prototype.send = function(body) {
			this.xhr.send(body);
		};
		XhrL2.prototype.abort = function() {
			this.xhr.abort();
		}
		XhrL2.prototype.setContentType = function(mimeType) {
			if ("setRequestHeader" in this.xhr) {
				this.xhr.setRequestHeader("Content-Type", mimeType);
			}
		}
		var XdrL2 = function(xdr) {
			this.xdr = xdr;
			xdr.onload = (function(l2) {
				return function() {
					var e;
					l2.responseText = xdr.responseText;
					if (xdr.contentType === "text/xml"
							|| xdr.contentType === "application/xml"
							|| /\/x-/.test(xdr.contentType)) {
						try {
							var xdoc = new ActiveXObject("Microsoft.XMLDOM");
							xdoc.loadXML(xdr.responseText);
							l2.responseXML = xdoc;
						} catch (e) {
							l2.responseXML = e;
						}
					}
					if (l2.onload) {
						l2.onload();
					}
				};
			})(this);
			xdr.onerror = (function(l2) {
				return function(event) {
					if (l2.onerror) {
						l2.onerror(event);
					}
				};
			})(this);
			xdr.ontimeout = (function(l2) {
				return function(event) {
					if (l2.onerror) {
						l2.onerror(event);
					}
				};
			})(this);
		};
		XdrL2.prototype.open = function(method, url) {
			this.xdr.open(method, url);
		};
		XdrL2.prototype.send = function(body) {
			this.xdr.send(body);
		};
		XdrL2.prototype.abort = function() {
			this.xdr.abort();
		};
		XdrL2.prototype.setContentType = function(mimeType) {
			// can't do it.
		};
		if (typeof XMLHttpRequest !== "undefined") {
			var xhr = new XMLHttpRequest();
			if ("withCredentials" in xhr) {
				return new XhrL2(xhr);
			}
		}
		if (typeof XDomainRequest !== "undefined") {
			return new XdrL2(new XDomainRequest());
		}
		if (typeof flensed.flXHR !== "undefined") {
			return new XhrL2(new flensed.flXHR({
				instancePooling : true
			}));
		}
		throw new Error("no cross-origin mechanism available");
	};
	// errHandler may be passed an XmlRpc.Fault or a thrown Error.
	XmlRpcClient.prototype.execute = function(req, resultHandler, errHandler) {
		(function(xClient) {
			var xhr;
			var e;
			try {
				xhr = XmlRpcClient.createXHR();
				xhr.open("POST", xClient.endpoint);
				xhr.setContentType("text/xml");
			} catch (e) {
				errHandler(e);
				throw e;
			}
			xhr.onload = function() {
				var xml = xhr.responseXML;
				var result;
				var e;
				if (xml) {
					try {
						result = XmlRpc.decodeResponse(xml);
					} catch (e) {
						if (errHandler) {
							errHandler(e);
						}
						return;
					}
				} else {
					if (errHandler) {
						errHandler("no XML response");
					}
					return;
				}
				if (result instanceof XmlRpc.Fault) {
					if (errHandler) {
						errHandler(result);
					}
				} else {
					if (resultHandler) {
						resultHandler(result);
					}
				}
			};
			xhr.onerror = function(event) {
				if (event) {
					event.toString = function() {
						return "No hub?";
					}
				} else {
					event = "No hub";
				}
				if (errHandler) {
					errHandler(event);
				}
			};
			xhr.send(req.toXml());
			return xhr;
		})(this);
	};

	var Message = function(mtype, params) {
		this["samp.mtype"] = mtype;
		this["samp.params"] = params;
	};

	var Connection = function(regInfo) {
		this.regInfo = regInfo;
		this.privateKey = regInfo["samp.private-key"];
		if (!typeof (this.privateKey) === "string") {
			throw new Error("Bad registration object");
		}
		this.xClient = new XmlRpcClient();
	};
	(function() {
		var connMethods = {
			call : [ TYPE_STRING, TYPE_STRING, TYPE_MAP ],
			callAll : [ TYPE_STRING, TYPE_MAP ],
			callAndWait : [ TYPE_STRING, TYPE_MAP, TYPE_STRING ],
			declareMetadata : [ TYPE_MAP ],
			declareSubscriptions : [ TYPE_MAP ],
			getMetadata : [ TYPE_STRING ],
			getRegisteredClients : [],
			getSubscribedClients : [ TYPE_STRING ],
			getSubscriptions : [ TYPE_STRING ],
			notify : [ TYPE_STRING, TYPE_MAP ],
			notifyAll : [ TYPE_MAP ],
			ping : [],
			reply : [ TYPE_STRING, TYPE_MAP ]
		};
		var fn;
		var types;
		for (fn in connMethods) {
			(function(fname, types) {
				// errHandler may be passed an XmlRpc.Fault or a thrown Error.
				Connection.prototype[fname] = function(sampArgs, resultHandler,
						errHandler) {
					var closer = (function(c) {
						return function() {
							c.close();
							throw "XmlRpc problem, connection closed.";
						}
					})(this);
					errHandler = errHandler || closer
					XmlRpc.checkParams(sampArgs, types);
					var request = new XmlRpcRequest(WEBSAMP_PREFIX + fname);
					request.addParam(this.privateKey);
					request.addParams(sampArgs);
					return this.xClient.execute(request, resultHandler,
							errHandler);
				};
			})(fn, connMethods[fn]);
		}
	})();
	Connection.prototype.unregister = function() {
		var e;
		if (this.callbackRequest) {
			try {
				this.callbackRequest.abort();
			} catch (e) {
			}
		}
		var request = new XmlRpcRequest(WEBSAMP_PREFIX + "unregister");
		request.addParam(this.privateKey);
		try {
			this.xClient.execute(request);
		} catch (e) {
			// log unregister failed
		}
		delete this.regInfo;
		delete this.privateKey;
	};
	Connection.prototype.close = function() {
		var e;
		if (this.closed) {
			return;
		}
		this.closed = true;
		try {
			if (this.regInfo) {
				this.unregister();
			}
		} catch (e) {
		}
		if (this.onclose) {
			oc = this.onclose;
			delete this.onclose;
			try {
				oc();
			} catch (e) {
			}
		}
	};
	Connection.prototype.setCallable = function(callableClient, successHandler) {
		var e;
		if (this.callbackRequest) {
			try {
				this.callbackRequest.abort();
			} catch (e) {
			} finally {
				delete this.callbackRequest;
			}
		}
		if (!callableClient && !this.regInfo) {
			return;
		}
		var request = new XmlRpcRequest(WEBSAMP_PREFIX
				+ "allowReverseCallbacks");
		request.addParam(this.privateKey);
		request.addParam(callableClient ? "1" : "0");
		var closer = (function(c) {
			return function() {
				c.close()
			}
		})(this);
		if (callableClient) {
			(function(connection) {
				var invokeCallback = function(callback) {
					var methodName = callback["samp.methodName"];
					var methodParams = callback["samp.params"];
					var handlerFunc = undefined;
					if (methodName === WEBSAMP_CLIENT_PREFIX
							+ "receiveNotification") {
						handlerFunc = callableClient.receiveNotification;
					} else if (methodName === WEBSAMP_CLIENT_PREFIX
							+ "receiveCall") {
						handlerFunc = callableClient.receiveCall;
					} else if (methodName === WEBSAMP_CLIENT_PREFIX
							+ "receiveResponse") {
						handlerFunc = callableClient.receiveResponse;
					} else {
						// unknown callback??
					}
					if (handlerFunc) {
						handlerFunc.apply(callableClient, methodParams);
					}
				};
				var startTime;
				var resultHandler = function(result) {
					if (getSampType(result) != TYPE_LIST) {
						errHandler(new Error("pullCallbacks result not List"));
						return;
					}
					var i;
					var e;
					for (i = 0; i < result.length; i++) {
						try {
							invokeCallback(result[i]);
						} catch (e) {
							// log here?
						}
					}
					callWaiter();
				};
				var errHandler = function(error) {
					var elapsed = new Date().getTime() - startTime;
					if (elapsed < 1000) {
						connection.close()
					} else {
						// probably a timeout
						callWaiter();
					}
				};
				var callWaiter = function() {
					if (!connection.regInfo) {
						return;
					}
					var request = new XmlRpcRequest(WEBSAMP_PREFIX
							+ "pullCallbacks");
					request.addParam(connection.privateKey);
					request.addParam("600");
					startTime = new Date().getTime();
					connection.callbackRequest = connection.xClient.execute(
							request, resultHandler, errHandler);
				};
				var sHandler = function() {
					callWaiter();
					successHandler();
				};
				connection.xClient.execute(request, sHandler, closer);
			})(this);
		} else {
			this.xClient.execute(request, successHandler, closer);
		}
	};
	Connection.prototype.translateUrl = function(url) {
		var translator = this.regInfo["samp.url-translator"] || "";
		return translator + url;
	};
	Connection.Action = function(actName, actArgs, resultKey) {
		this.actName = actName;
		this.actArgs = actArgs;
		this.resultKey = resultKey;
	};

	var CallableClient = function(connection) {
		this.callHandler = {};
		this.replyHandler = {};
	};
	CallableClient.prototype.init = function(connection) {
	};
	CallableClient.prototype.receiveNotification = function(senderId, message) {
		var mtype = message["samp.mtype"];
		var handled = false;
		var e;
		if (mtype in this.callHandler) {
			try {
				this.callHandler[mtype](senderId, message, false);
			} catch (e) {
			}
			handled = true;
		}
		return handled;
	};
	CallableClient.prototype.receiveCall = function(senderId, msgId, message) {
		var mtype = message["samp.mtype"];
		var handled = false;
		var response;
		var result;
		var e;
		if (mtype in this.callHandler) {
			try {
				result = this.callHandler[mtype](senderId, message, true) || {};
				response = {
					"samp.status" : "samp.ok",
					"samp.result" : result
				};
				handled = true;
			} catch (e) {
				response = {
					"samp.status" : "samp.error",
					"samp.error" : {
						"samp.errortxt" : e.toString()
					}
				};
			}
		} else {
			response = {
				"samp.status" : "samp.warning",
				"samp.result" : {},
				"samp.error" : {
					"samp.errortxt" : "no action"
				}
			};
		}
		this.connection.reply([ msgId, response ]);
		return handled;
	};
	CallableClient.prototype.receiveResponse = function(responderId, msgTag,
			response) {
		var handled = false;
		var e;
		if (msgTag in this.replyHandler) {
			try {
				this.replyHandler[msgTag](responderId, msgTag, response);
				handled = true;
			} catch (e) {
			}
		}
		return handled;
	};
	CallableClient.prototype.calculateSubscriptions = function() {
		var subs = {};
		var mt;
		for (mt in this.callHandler) {
			subs[mt] = {};
		}
		return subs;
	};

	// ClientTracker is a CallableClient which also provides tracking of
	// registered clients.
	var ClientTracker = function() {
		var tracker = this;
		this.ids = {};
		this.metas = {};
		this.subs = {};
		this.replyHandler = {};
		this.callHandler = {
			"samp.hub.event.shutdown" : function(senderId, message) {
				tracker.connection.close();
			},
			"samp.hub.disconnect" : function(senderId, message) {
				tracker.connection.close();
			},
			"samp.hub.event.register" : function(senderId, message) {
				var id = message["samp.params"]["id"];
				tracker.ids[id] = true;
				tracker.changed(id, "register", null);
			},
			"samp.hub.event.unregister" : function(senderId, message) {
				var id = message["samp.params"]["id"];
				delete tracker.ids[id];
				delete tracker.metas[id];
				delete tracker.subs[id];
				tracker.changed(id, "unregister", null);
			},
			"samp.hub.event.metadata" : function(senderId, message) {
				var id = message["samp.params"]["id"];
				var meta = message["samp.params"]["metadata"];
				tracker.metas[id] = meta;
				tracker.changed(id, "meta", meta);
			},
			"samp.hub.event.subscriptions" : function(senderId, message) {
				var id = message["samp.params"]["id"];
				var subs = message["samp.params"]["subscriptions"];
				tracker.subs[id] = subs;
				tracker.changed(id, "subs", subs);
			}
		};
	};
	ClientTracker.prototype = heir(CallableClient.prototype);
	ClientTracker.prototype.changed = function(id, type, data) {
		if (this.onchange) {
			this.onchange(id, type, data);
		}
	};
	ClientTracker.prototype.init = function(connection) {
		var tracker = this;
		this.connection = connection;
		var retrieveInfo = function(id, type, infoFuncName, infoArray) {
			connection[infoFuncName]([ id ], function(info) {
				infoArray[id] = info;
				tracker.changed(id, type, info);
			});
		};
		connection.getRegisteredClients([], function(idlist) {
			var i;
			var id;
			tracker.ids = {};
			for (i = 0; i < idlist.length; i++) {
				id = idlist[i];
				tracker.ids[id] = true;
				retrieveInfo(id, "meta", "getMetadata", tracker.metas);
				retrieveInfo(id, "subs", "getSubscriptions", tracker.subs);
			}
			tracker.changed(null, "ids", null);
		});
	};
	ClientTracker.prototype.getName = function(id) {
		var meta = this.metas[id];
		return (meta && meta["samp.name"]) ? meta["samp.name"] : "[" + id + "]";
	};

	var Connector = function(name, meta, callableClient, subs) {
		this.name = name;
		this.meta = meta;
		this.callableClient = callableClient;
		this.subs = subs;
		this.regTextNodes = [];
		this.whenRegs = [];
		this.whenUnregs = [];
		this.connection = undefined;
		this.onreg = undefined;
		this.onunreg = undefined;
	};
	var setRegText = function(connector, txt) {
		var i;
		var nodes = connector.regTextNodes;
		var node;
		for (i = 0; i < nodes.length; i++) {
			node = nodes[i];
			node.innerHTML = "";
			node.appendChild(document.createTextNode(txt));
		}
	};
	Connector.prototype.setConnection = function(conn) {
		var connector = this;
		var e;
		if (this.connection) {
			this.connection.close();
			if (this.onunreg) {
				try {
					this.onunreg();
				} catch (e) {
				}
			}
		}
		this.connection = conn;
		if (conn) {
			conn.onclose = function() {
				connector.connection = null;
				if (connector.onunreg) {
					try {
						connector.onunreg();
					} catch (e) {
					}
				}
				connector.update();
			};
			if (this.meta) {
				conn.declareMetadata([ this.meta ]);
			}
			if (this.callableClient) {
				if (this.callableClient.init) {
					this.callableClient.init(conn);
				}
				conn.setCallable(this.callableClient, function() {
					conn.declareSubscriptions([ connector.subs ]);
				});
			}
			if (this.onreg) {
				try {
					this.onreg(conn);
				} catch (e) {
				}
			}
		}
		this.update();
	};
	Connector.prototype.register = function() {
		var connector = this;
		var regErrHandler = function(err) {
			setRegText(connector, "no (" + err.toString() + ")");
		};
		var regSuccessHandler = function(conn) {
			connector.setConnection(conn);
			setRegText(connector, conn ? "Yes" : "No");
		};
		register(this.name, regSuccessHandler, regErrHandler);
	};
	Connector.prototype.unregister = function() {
		if (this.connection) {
			this.connection.unregister([]);
			this.setConnection(null);
		}
	};
	Connector.prototype.createRegButtons = function() {
		var connector = this;
		var regButt = document.createElement("button");
		regButt.setAttribute("type", "button");
		regButt.appendChild(document.createTextNode("Register"));
		regButt.onclick = function() {
			connector.register();
		};
		this.whenUnregs.push(regButt);
		var unregButt = document.createElement("button");
		unregButt.setAttribute("type", "button");
		unregButt.appendChild(document.createTextNode("Unregister"));
		unregButt.onclick = function() {
			connector.unregister();
		};
		this.whenRegs.push(unregButt);
		var regText = document.createElement("span");
		this.regTextNodes.push(regText);
		var node = document.createDocumentFragment();
		node.appendChild(regButt);
		node.appendChild(document.createTextNode(" "));
		node.appendChild(unregButt);
		var label = document.createElement("span");
		label.innerHTML = " <strong>Registered: </strong>";
		node.appendChild(label);
		node.appendChild(regText);
		this.update();
		return node;
	};
	Connector.prototype.update = function() {
		var i;
		var isConnected = !!this.connection;
		var enableds = isConnected ? this.whenRegs : this.whenUnregs;
		var disableds = isConnected ? this.whenUnregs : this.whenRegs;
		for (i = 0; i < enableds.length; i++) {
			enableds[i].removeAttribute("disabled");
		}
		for (i = 0; i < disableds.length; i++) {
			disableds[i].setAttribute("disabled", "disabled");
		}
		setRegText(this, "No");
	};

	var isSubscribed = function(subs, mtype) {
		var matching = function(pattern, mtype) {
			if (pattern == mtype) {
				return true;
			} else if (pattern === "*") {
				return true;
			} else {
				var prefix;
				var split = /^(.*)\.\*$/.exec(pat);
				if (split) {
					prefix = split[1];
					if (prefix === mtype.substring(0, prefix.length)) {
						return true;
					}
				}
			}
			return false;
		};
		var pat;
		for (pat in subs) {
			if (matching(pat, mtype)) {
				return true;
			}
		}
		return false;
	}

	var register = function(appName, connectionHandler, errorHandler) {
		var xClient = new XmlRpcClient();
		var regRequest = new XmlRpcRequest(WEBSAMP_PREFIX + "register");
		var securityInfo = {
			"samp.name" : appName
		};
		regRequest.addParam(securityInfo);
		regRequest.checkParams([ TYPE_MAP ]);
		var resultHandler = function(result) {
			var conn;
			var e;
			try {
				conn = new Connection(result, 1000);
			} catch (e) {
				errorHandler(e);
				return;
			}
			connectionHandler(conn);
		};
		xClient.execute(regRequest, resultHandler, errorHandler);
	};

	/* Exports. */
	var jss = {};
	jss.XmlRpcRequest = XmlRpcRequest;
	jss.XmlRpcClient = XmlRpcClient;
	jss.Message = Message;
	jss.TYPE_STRING = TYPE_STRING;
	jss.TYPE_LIST = TYPE_LIST;
	jss.TYPE_MAP = TYPE_MAP;
	jss.register = register;
	jss.isSubscribed = isSubscribed;
	jss.Connector = Connector;
	jss.CallableClient = CallableClient;
	jss.ClientTracker = ClientTracker;

	return jss;
})();
