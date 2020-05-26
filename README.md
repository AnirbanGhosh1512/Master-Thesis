# Master-Thesis
The logistics system and the production steps are separate modules. The product needs 4 production steps, which can be performed by the production modules. Every production module has its own processing time t. The production module operates with a carrier which can only move in circles. The carrier can always carry only one product which is removed by the production modules while they are processed, and returned to the carrier when they are finished. After the product has completed with all necessary production steps, it needs to be brought to the product removal where it is removed from production.

This is basically the layout for a simplified production line. The production modules can be switched, but there can never be more than 4 modules on the transport system, and not more than 2 in a row. The carrier has a constant speed v (acceleration can be neglected).

The explicit production times vary for each module, but are variables for now. Orders are given by customers and do not always require all production steps (step 2 and 4 are not required for all orders). However, Production step 1 has to be done before 3, and 2 before 3 (if it is required in the order).
