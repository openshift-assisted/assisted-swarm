// Code generated by go-swagger; DO NOT EDIT.

package swarm

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	"net/http"

	"github.com/go-openapi/runtime"

	"github.com/openshift-assisted/assisted-swarm/models"
)

// DeleteAgentNoContentCode is the HTTP code returned for type DeleteAgentNoContent
const DeleteAgentNoContentCode int = 204

/*DeleteAgentNoContent Success

swagger:response deleteAgentNoContent
*/
type DeleteAgentNoContent struct {
}

// NewDeleteAgentNoContent creates DeleteAgentNoContent with default headers values
func NewDeleteAgentNoContent() *DeleteAgentNoContent {

	return &DeleteAgentNoContent{}
}

// WriteResponse to the client
func (o *DeleteAgentNoContent) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.Header().Del(runtime.HeaderContentType) //Remove Content-Type on empty responses

	rw.WriteHeader(204)
}

// DeleteAgentBadRequestCode is the HTTP code returned for type DeleteAgentBadRequest
const DeleteAgentBadRequestCode int = 400

/*DeleteAgentBadRequest Error.

swagger:response deleteAgentBadRequest
*/
type DeleteAgentBadRequest struct {

	/*
	  In: Body
	*/
	Payload *models.Error `json:"body,omitempty"`
}

// NewDeleteAgentBadRequest creates DeleteAgentBadRequest with default headers values
func NewDeleteAgentBadRequest() *DeleteAgentBadRequest {

	return &DeleteAgentBadRequest{}
}

// WithPayload adds the payload to the delete agent bad request response
func (o *DeleteAgentBadRequest) WithPayload(payload *models.Error) *DeleteAgentBadRequest {
	o.Payload = payload
	return o
}

// SetPayload sets the payload to the delete agent bad request response
func (o *DeleteAgentBadRequest) SetPayload(payload *models.Error) {
	o.Payload = payload
}

// WriteResponse to the client
func (o *DeleteAgentBadRequest) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.WriteHeader(400)
	if o.Payload != nil {
		payload := o.Payload
		if err := producer.Produce(rw, payload); err != nil {
			panic(err) // let the recovery middleware deal with this
		}
	}
}

// DeleteAgentUnauthorizedCode is the HTTP code returned for type DeleteAgentUnauthorized
const DeleteAgentUnauthorizedCode int = 401

/*DeleteAgentUnauthorized Unauthorized.

swagger:response deleteAgentUnauthorized
*/
type DeleteAgentUnauthorized struct {

	/*
	  In: Body
	*/
	Payload *models.Error `json:"body,omitempty"`
}

// NewDeleteAgentUnauthorized creates DeleteAgentUnauthorized with default headers values
func NewDeleteAgentUnauthorized() *DeleteAgentUnauthorized {

	return &DeleteAgentUnauthorized{}
}

// WithPayload adds the payload to the delete agent unauthorized response
func (o *DeleteAgentUnauthorized) WithPayload(payload *models.Error) *DeleteAgentUnauthorized {
	o.Payload = payload
	return o
}

// SetPayload sets the payload to the delete agent unauthorized response
func (o *DeleteAgentUnauthorized) SetPayload(payload *models.Error) {
	o.Payload = payload
}

// WriteResponse to the client
func (o *DeleteAgentUnauthorized) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.WriteHeader(401)
	if o.Payload != nil {
		payload := o.Payload
		if err := producer.Produce(rw, payload); err != nil {
			panic(err) // let the recovery middleware deal with this
		}
	}
}

// DeleteAgentForbiddenCode is the HTTP code returned for type DeleteAgentForbidden
const DeleteAgentForbiddenCode int = 403

/*DeleteAgentForbidden Forbidden.

swagger:response deleteAgentForbidden
*/
type DeleteAgentForbidden struct {

	/*
	  In: Body
	*/
	Payload *models.Error `json:"body,omitempty"`
}

// NewDeleteAgentForbidden creates DeleteAgentForbidden with default headers values
func NewDeleteAgentForbidden() *DeleteAgentForbidden {

	return &DeleteAgentForbidden{}
}

// WithPayload adds the payload to the delete agent forbidden response
func (o *DeleteAgentForbidden) WithPayload(payload *models.Error) *DeleteAgentForbidden {
	o.Payload = payload
	return o
}

// SetPayload sets the payload to the delete agent forbidden response
func (o *DeleteAgentForbidden) SetPayload(payload *models.Error) {
	o.Payload = payload
}

// WriteResponse to the client
func (o *DeleteAgentForbidden) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.WriteHeader(403)
	if o.Payload != nil {
		payload := o.Payload
		if err := producer.Produce(rw, payload); err != nil {
			panic(err) // let the recovery middleware deal with this
		}
	}
}

// DeleteAgentNotFoundCode is the HTTP code returned for type DeleteAgentNotFound
const DeleteAgentNotFoundCode int = 404

/*DeleteAgentNotFound Not Found.

swagger:response deleteAgentNotFound
*/
type DeleteAgentNotFound struct {

	/*
	  In: Body
	*/
	Payload *models.Error `json:"body,omitempty"`
}

// NewDeleteAgentNotFound creates DeleteAgentNotFound with default headers values
func NewDeleteAgentNotFound() *DeleteAgentNotFound {

	return &DeleteAgentNotFound{}
}

// WithPayload adds the payload to the delete agent not found response
func (o *DeleteAgentNotFound) WithPayload(payload *models.Error) *DeleteAgentNotFound {
	o.Payload = payload
	return o
}

// SetPayload sets the payload to the delete agent not found response
func (o *DeleteAgentNotFound) SetPayload(payload *models.Error) {
	o.Payload = payload
}

// WriteResponse to the client
func (o *DeleteAgentNotFound) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.WriteHeader(404)
	if o.Payload != nil {
		payload := o.Payload
		if err := producer.Produce(rw, payload); err != nil {
			panic(err) // let the recovery middleware deal with this
		}
	}
}

// DeleteAgentInternalServerErrorCode is the HTTP code returned for type DeleteAgentInternalServerError
const DeleteAgentInternalServerErrorCode int = 500

/*DeleteAgentInternalServerError Error.

swagger:response deleteAgentInternalServerError
*/
type DeleteAgentInternalServerError struct {

	/*
	  In: Body
	*/
	Payload *models.Error `json:"body,omitempty"`
}

// NewDeleteAgentInternalServerError creates DeleteAgentInternalServerError with default headers values
func NewDeleteAgentInternalServerError() *DeleteAgentInternalServerError {

	return &DeleteAgentInternalServerError{}
}

// WithPayload adds the payload to the delete agent internal server error response
func (o *DeleteAgentInternalServerError) WithPayload(payload *models.Error) *DeleteAgentInternalServerError {
	o.Payload = payload
	return o
}

// SetPayload sets the payload to the delete agent internal server error response
func (o *DeleteAgentInternalServerError) SetPayload(payload *models.Error) {
	o.Payload = payload
}

// WriteResponse to the client
func (o *DeleteAgentInternalServerError) WriteResponse(rw http.ResponseWriter, producer runtime.Producer) {

	rw.WriteHeader(500)
	if o.Payload != nil {
		payload := o.Payload
		if err := producer.Produce(rw, payload); err != nil {
			panic(err) // let the recovery middleware deal with this
		}
	}
}
