// Code generated by go-swagger; DO NOT EDIT.

package swarm

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the swagger generate command

import (
	"context"
	"net/http"
	"time"

	"github.com/go-openapi/errors"
	"github.com/go-openapi/runtime"
	cr "github.com/go-openapi/runtime/client"
	"github.com/go-openapi/strfmt"
	"github.com/go-openapi/swag"
)

// NewGetAgentParams creates a new GetAgentParams object,
// with the default timeout for this client.
//
// Default values are not hydrated, since defaults are normally applied by the API server side.
//
// To enforce default values in parameter, use SetDefaults or WithDefaults.
func NewGetAgentParams() *GetAgentParams {
	return &GetAgentParams{
		timeout: cr.DefaultTimeout,
	}
}

// NewGetAgentParamsWithTimeout creates a new GetAgentParams object
// with the ability to set a timeout on a request.
func NewGetAgentParamsWithTimeout(timeout time.Duration) *GetAgentParams {
	return &GetAgentParams{
		timeout: timeout,
	}
}

// NewGetAgentParamsWithContext creates a new GetAgentParams object
// with the ability to set a context for a request.
func NewGetAgentParamsWithContext(ctx context.Context) *GetAgentParams {
	return &GetAgentParams{
		Context: ctx,
	}
}

// NewGetAgentParamsWithHTTPClient creates a new GetAgentParams object
// with the ability to set a custom HTTPClient for a request.
func NewGetAgentParamsWithHTTPClient(client *http.Client) *GetAgentParams {
	return &GetAgentParams{
		HTTPClient: client,
	}
}

/* GetAgentParams contains all the parameters to send to the API endpoint
   for the get agent operation.

   Typically these are written to a http.Request.
*/
type GetAgentParams struct {

	// AgentID.
	AgentID int64

	timeout    time.Duration
	Context    context.Context
	HTTPClient *http.Client
}

// WithDefaults hydrates default values in the get agent params (not the query body).
//
// All values with no default are reset to their zero value.
func (o *GetAgentParams) WithDefaults() *GetAgentParams {
	o.SetDefaults()
	return o
}

// SetDefaults hydrates default values in the get agent params (not the query body).
//
// All values with no default are reset to their zero value.
func (o *GetAgentParams) SetDefaults() {
	// no default values defined for this parameter
}

// WithTimeout adds the timeout to the get agent params
func (o *GetAgentParams) WithTimeout(timeout time.Duration) *GetAgentParams {
	o.SetTimeout(timeout)
	return o
}

// SetTimeout adds the timeout to the get agent params
func (o *GetAgentParams) SetTimeout(timeout time.Duration) {
	o.timeout = timeout
}

// WithContext adds the context to the get agent params
func (o *GetAgentParams) WithContext(ctx context.Context) *GetAgentParams {
	o.SetContext(ctx)
	return o
}

// SetContext adds the context to the get agent params
func (o *GetAgentParams) SetContext(ctx context.Context) {
	o.Context = ctx
}

// WithHTTPClient adds the HTTPClient to the get agent params
func (o *GetAgentParams) WithHTTPClient(client *http.Client) *GetAgentParams {
	o.SetHTTPClient(client)
	return o
}

// SetHTTPClient adds the HTTPClient to the get agent params
func (o *GetAgentParams) SetHTTPClient(client *http.Client) {
	o.HTTPClient = client
}

// WithAgentID adds the agentID to the get agent params
func (o *GetAgentParams) WithAgentID(agentID int64) *GetAgentParams {
	o.SetAgentID(agentID)
	return o
}

// SetAgentID adds the agentId to the get agent params
func (o *GetAgentParams) SetAgentID(agentID int64) {
	o.AgentID = agentID
}

// WriteToRequest writes these params to a swagger request
func (o *GetAgentParams) WriteToRequest(r runtime.ClientRequest, reg strfmt.Registry) error {

	if err := r.SetTimeout(o.timeout); err != nil {
		return err
	}
	var res []error

	// path param agent_id
	if err := r.SetPathParam("agent_id", swag.FormatInt64(o.AgentID)); err != nil {
		return err
	}

	if len(res) > 0 {
		return errors.CompositeValidationError(res...)
	}
	return nil
}
