// Code generated by go-swagger; DO NOT EDIT.

package swarm

// This file was generated by the swagger tool.
// Editing this file might prove futile when you re-run the generate command

import (
	"net/http"

	"github.com/go-openapi/runtime/middleware"
)

// CreateNewAgentHandlerFunc turns a function with the right signature into a create new agent handler
type CreateNewAgentHandlerFunc func(CreateNewAgentParams) middleware.Responder

// Handle executing the request and returning a response
func (fn CreateNewAgentHandlerFunc) Handle(params CreateNewAgentParams) middleware.Responder {
	return fn(params)
}

// CreateNewAgentHandler interface for that can handle valid create new agent params
type CreateNewAgentHandler interface {
	Handle(CreateNewAgentParams) middleware.Responder
}

// NewCreateNewAgent creates a new http.Handler for the create new agent operation
func NewCreateNewAgent(ctx *middleware.Context, handler CreateNewAgentHandler) *CreateNewAgent {
	return &CreateNewAgent{Context: ctx, Handler: handler}
}

/* CreateNewAgent swagger:route POST /agents swarm createNewAgent

Create new agent.

*/
type CreateNewAgent struct {
	Context *middleware.Context
	Handler CreateNewAgentHandler
}

func (o *CreateNewAgent) ServeHTTP(rw http.ResponseWriter, r *http.Request) {
	route, rCtx, _ := o.Context.RouteInfo(r)
	if rCtx != nil {
		*r = *rCtx
	}
	var Params = NewCreateNewAgentParams()
	if err := o.Context.BindValidRequest(r, route, &Params); err != nil { // bind params
		o.Context.Respond(rw, r, route.Produces, route, err)
		return
	}

	res := o.Handler.Handle(Params) // actually handle the request
	o.Context.Respond(rw, r, route.Produces, route, res)

}