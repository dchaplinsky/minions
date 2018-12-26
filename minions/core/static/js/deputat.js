/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 5);
/******/ })
/************************************************************************/
/******/ ({

/***/ 5:
/***/ (function(module, exports, __webpack_require__) {

"use strict";
(function () {
    var dropdown = document.getElementById('drop_down');
    var showmore = document.getElementById('show_more');
    var panewraps = document.querySelectorAll('div.bottom_block.list_persons.cf div.wrap_block.cf');

    var btn = document.createElement('div');

    if (dropdown) {
        btn.classList.add('drop_down_open');
        btn.innerHTML = dropdown.querySelector('li.active a').innerHTML;
        btn.onclick = function () {
            if (dropdown.classList.contains('open')) {
                dropdown.classList.remove('open');
                btn.classList.remove('open');
            } else {
                dropdown.classList.add('open');
                btn.classList.add('open');
            }
        };
        dropdown.parentNode.insertBefore(btn, dropdown);var _loop = function _loop(
        i) {
            dropdown.children[i].onclick = function () {
                btn.innerHTML = dropdown.children[i].innerText;
                dropdown.classList.remove('open');
            };};for (var i = 0; i < dropdown.children.length; i++) {_loop(i);
        }

    }

    if (showmore) {

        showmore.onclick = function () {
            for (var i = 0; i < panewraps.length; i++) {
                if (panewraps[i].classList.contains('open')) {
                    panewraps[i].classList.remove('open');
                    showmore.classList.remove('open');
                    showmore.innerHTML = "Показати більше";
                } else {
                    panewraps[i].classList.add('open');
                    showmore.classList.add('open');
                    showmore.innerHTML = "Показати менше";
                }

            }
        };
    }





})();

/***/ })

/******/ });
//# sourceMappingURL=deputat.js.map